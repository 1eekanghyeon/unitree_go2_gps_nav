#!/usr/bin/env python3

import osmnx as ox
import networkx as nx
import folium
import utm
import math
from shapely.geometry import Polygon, Point, box
import numpy as np
import heapq 
import geopandas as gpd
import pyproj 
from scipy.ndimage import binary_dilation # 장애물 확장을 위해 추가

# osmnx 상세 로그 출력 (필요시 주석 해제)
# ox.settings.log_console = True

# --- 1. GridMap 클래스 정의 (이전과 동일) ---
class GridMap:
    def __init__(self, width_m, height_m, resolution_m, origin_utm_e, origin_utm_n, zone_number, zone_letter, utm_crs_epsg):
        self.width_m = width_m
        self.height_m = height_m
        self.resolution = resolution_m
        self.origin_e = origin_utm_e
        self.origin_n = origin_utm_n
        self.zone_number = zone_number
        self.zone_letter = zone_letter
        self.utm_crs_epsg = utm_crs_epsg

        self.grid_width = int(math.ceil(width_m / resolution_m))
        self.grid_height = int(math.ceil(height_m / resolution_m))
        
        self.data = np.zeros((self.grid_height, self.grid_width), dtype=np.uint8)
        print(f"GridMap created: {self.grid_width}x{self.grid_height} cells, resolution: {self.resolution}m")
        print(f"GridMap UTM origin (bottom-left): E={self.origin_e:.2f}, N={self.origin_n:.2f} (Zone {self.zone_number}{self.zone_letter}, EPSG:{self.utm_crs_epsg})")
        print(f"GridMap UTM extent: E=[{self.origin_e:.2f}, {self.origin_e + self.width_m:.2f}], "
              f"N=[{self.origin_n:.2f}, {self.origin_n + self.height_m:.2f}]")

    def utm_to_grid_coords(self, utm_e, utm_n):
        grid_x = int((utm_e - self.origin_e) / self.resolution)
        grid_y = int((utm_n - self.origin_n) / self.resolution)
        return grid_x, grid_y

    def grid_coords_to_utm(self, grid_x, grid_y):
        utm_e = self.origin_e + (grid_x + 0.5) * self.resolution
        utm_n = self.origin_n + (grid_y + 0.5) * self.resolution
        return utm_e, utm_n

    def is_valid_grid_coords(self, grid_x, grid_y):
        return 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height

    def set_obstacle_from_utm_polygon(self, shapely_polygon_utm):
        if not shapely_polygon_utm.is_valid:
            shapely_polygon_utm = shapely_polygon_utm.buffer(0)
            if not shapely_polygon_utm.is_valid:
                # print(f"Warning: Polygon still invalid after buffer(0). Skipping this obstacle.")
                return

        min_e_poly, min_n_poly, max_e_poly, max_n_poly = shapely_polygon_utm.bounds
        
        start_gx_mbr, start_gy_mbr = self.utm_to_grid_coords(min_e_poly, min_n_poly)
        end_gx_mbr, end_gy_mbr = self.utm_to_grid_coords(max_e_poly, max_n_poly)

        final_gx_min = max(0, min(start_gx_mbr, end_gx_mbr))
        final_gy_min = max(0, min(start_gy_mbr, end_gy_mbr))
        final_gx_max = min(self.grid_width - 1, max(start_gx_mbr, end_gx_mbr))
        final_gy_max = min(self.grid_height - 1, max(start_gy_mbr, end_gy_mbr))

        if final_gx_min > final_gx_max or final_gy_min > final_gy_max:
            return 

        obstacle_cells_count = 0
        for gy in range(final_gy_min, final_gy_max + 1):
            for gx in range(final_gx_min, final_gx_max + 1):
                cell_center_e, cell_center_n = self.grid_coords_to_utm(gx, gy)
                cell_center_point_utm = Point(cell_center_e, cell_center_n)
                
                if shapely_polygon_utm.intersects(cell_center_point_utm):
                    if self.is_valid_grid_coords(gx, gy):
                        self.data[gy, gx] = 1
                        obstacle_cells_count += 1
        # if obstacle_cells_count > 0: # 로그가 너무 많을 수 있어 주석 처리
            # print(f"Rasterized polygon obstacle: {obstacle_cells_count} cells marked.")

    def inflate_obstacles(self, clearance_m):
        """장애물을 지정된 거리만큼 확장합니다."""
        if clearance_m <= 0:
            return
        
        clearance_cells = math.ceil(clearance_m / self.resolution)
        if clearance_cells <= 0:
            return

        print(f"Inflating obstacles by {clearance_m}m ({clearance_cells} cells)...")
        
        # binary_dilation은 True/False 배열에 대해 작동하므로, 0/1 배열을 bool 배열로 변환
        obstacle_mask = self.data.astype(bool)
        
        # 구조 요소(structuring element) 생성: 원형에 가까운 확장을 위해 disk 모양 사용
        # 또는 간단하게 여러 번 반복(iterations)하는 방식도 가능
        # iterations = clearance_cells
        # inflated_mask = binary_dilation(obstacle_mask, iterations=iterations)
        
        # Disk-like structuring element
        y, x = np.ogrid[-clearance_cells:clearance_cells+1, -clearance_cells:clearance_cells+1]
        disk_structure = x**2 + y**2 <= clearance_cells**2
        
        inflated_mask = binary_dilation(obstacle_mask, structure=disk_structure)
        
        self.data = inflated_mask.astype(np.uint8)
        print("Obstacles inflated.")


# --- 2. A* 알고리즘 구현 (이전과 동일) ---
def heuristic(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def a_star_search(grid_map_obj, start_grid_coords, goal_grid_coords):
    # ... (이전 A* 알고리즘 코드와 동일) ...
    if not grid_map_obj.is_valid_grid_coords(start_grid_coords[0], start_grid_coords[1]) or \
       not grid_map_obj.is_valid_grid_coords(goal_grid_coords[0], goal_grid_coords[1]):
        print("Error: Start or Goal grid coordinates are out of bounds.")
        return None
    if grid_map_obj.data[start_grid_coords[1], start_grid_coords[0]] == 1:
        print(f"Error: Start node {start_grid_coords} is on an (inflated) obstacle.")
        return None
    if grid_map_obj.data[goal_grid_coords[1], goal_grid_coords[0]] == 1:
        print(f"Error: Goal node {goal_grid_coords} is on an (inflated) obstacle.")
        return None

    neighbors = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]

    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start_grid_coords, goal_grid_coords), 0, start_grid_coords)) 

    came_from = {}
    g_score = {start_grid_coords: 0}

    explored_count = 0
    while open_set:
        current_f, current_g, current_node = heapq.heappop(open_set)
        explored_count += 1

        if current_node == goal_grid_coords:
            print(f"A* path found! Explored {explored_count} nodes.")
            path = []
            temp_node = current_node
            while temp_node in came_from:
                path.append(temp_node)
                temp_node = came_from[temp_node]
            path.append(start_grid_coords)
            return path[::-1]

        for dx, dy in neighbors:
            neighbor = (current_node[0] + dx, current_node[1] + dy)
            if not grid_map_obj.is_valid_grid_coords(neighbor[0], neighbor[1]) or \
               grid_map_obj.data[neighbor[1], neighbor[0]] == 1:
                continue

            move_cost = 1.414 if abs(dx) == 1 and abs(dy) == 1 else 1.0
            tentative_g_score = current_g + move_cost

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score_neighbor = tentative_g_score + heuristic(neighbor, goal_grid_coords)
                heapq.heappush(open_set, (f_score_neighbor, tentative_g_score, neighbor))
    
    print(f"A* failed to find a path after exploring {explored_count} nodes.")
    return None


# --- 3. 메인 실행 부분 ---
if __name__ == '__main__':
    start_lat, start_lon = 34.776694, 127.700792
    goal_lat, goal_lon = 34.776696, 127.700427

    lat_buffer = 0.0010 
    lon_buffer = 0.0010 

    s_lat_bbox, n_lat_bbox = sorted([start_lat, goal_lat])
    w_lon_bbox, e_lon_bbox = sorted([start_lon, goal_lon])
    
    query_north = n_lat_bbox + lat_buffer
    query_south = s_lat_bbox - lat_buffer
    query_east = e_lon_bbox + lon_buffer
    query_west = w_lon_bbox - lon_buffer
    
    print(f"Path planning from ({start_lat:.6f},{start_lon:.6f}) to ({goal_lat:.6f},{goal_lon:.6f})")
    print(f"OSM Query BBox: N={query_north:.6f}, S={query_south:.6f}, E={query_east:.6f}, W={query_west:.6f}")

    query_polygon_wgs84 = Polygon([(query_west, query_south), (query_west, query_north),
                                   (query_east, query_north), (query_east, query_south)])

    if not query_polygon_wgs84.is_valid or query_polygon_wgs84.area == 0:
        print("CRITICAL ERROR: Query polygon for OSM is invalid or has zero area.")
        exit()
    print(f"Query polygon created. Is valid: {query_polygon_wgs84.is_valid}, Area (deg^2): {query_polygon_wgs84.area:.8f}")

    grid_resolution_m = 0.25  # 해상도를 약간 더 높임 (0.5m -> 0.25m)
    obstacle_clearance_m = 1.8 # 장애물로부터 유지할 최소 거리 (미터) - 로봇 크기 + 안전 여유 고려

    temp_e, temp_n, zone_num, zone_letter = utm.from_latlon(start_lat, start_lon)
    
    is_southern_hemisphere = zone_letter < 'N'
    target_crs_epsg_code = 0
    if zone_num > 0:
        target_crs_epsg_code = 32600 + zone_num if not is_southern_hemisphere else 32700 + zone_num
        target_crs_string = f"EPSG:{target_crs_epsg_code}"
        print(f"Determined Target CRS for UTM projection: {target_crs_string} (Zone {zone_num}{zone_letter})")
    else:
        print(f"Could not determine valid EPSG code for UTM Zone {zone_num}{zone_letter}. Exiting.")
        exit()

    grid_origin_e_utm, grid_origin_n_utm, _, _ = utm.from_latlon(query_south, query_west, 
                                                               force_zone_number=zone_num, force_zone_letter=zone_letter)
    grid_top_right_e_utm, grid_top_right_n_utm, _, _ = utm.from_latlon(query_north, query_east,
                                                                     force_zone_number=zone_num, force_zone_letter=zone_letter)
    
    map_width_m = grid_top_right_e_utm - grid_origin_e_utm
    map_height_m = grid_top_right_n_utm - grid_origin_n_utm

    if map_width_m <= 0 or map_height_m <= 0:
        print(f"CRITICAL ERROR: Map width ({map_width_m:.2f}m) or height ({map_height_m:.2f}m) is zero or negative. Check query bounds.")
        exit()

    grid_map = GridMap(map_width_m, map_height_m, grid_resolution_m, 
                       grid_origin_e_utm, grid_origin_n_utm, zone_num, zone_letter, target_crs_epsg_code)

    common_tags = {'leisure': ['park', 'garden', 'playground'],
                   'landuse': ['grass', 'meadow', 'village_green', 'recreation_ground', 'cemetery', 'construction', 'farmland', 'forest'],
                   'natural': ['wood', 'scrub', 'heath', 'water', 'wetland', 'beach', 'sand'],
                   'building': True,
                   'amenity': ['parking', 'school', 'university', 'hospital', 'place_of_worship'],
                   'barrier': True, 'power': ['plant', 'substation'], 'man_made': ['wastewater_plant', 'works']}
    output_html_filename = "osm_astar_path_inflated_visualization.html"

    try:
        print("Fetching features from OSM...")
        features_gdf_wgs84 = ox.features_from_polygon(query_polygon_wgs84, tags=common_tags)
        print(f"Found {len(features_gdf_wgs84)} features from OSM.")

        if not features_gdf_wgs84.empty and 'geometry' in features_gdf_wgs84.columns:
            print(f"Projecting features to target CRS: {target_crs_string}")
            features_utm_gdf = features_gdf_wgs84.to_crs(target_crs_string)
            print(f"Rasterizing {len(features_utm_gdf)} features onto grid...")
            for index, feature_row in features_utm_gdf.iterrows():
                geom_utm = feature_row['geometry']
                if geom_utm and geom_utm.is_valid:
                    if geom_utm.geom_type == 'Polygon':
                        grid_map.set_obstacle_from_utm_polygon(geom_utm)
                    elif geom_utm.geom_type == 'MultiPolygon':
                        for poly_utm in geom_utm.geoms:
                            if poly_utm.is_valid:
                                grid_map.set_obstacle_from_utm_polygon(poly_utm)
            
            # *** 장애물 확장(Inflation) 수행 ***
            grid_map.inflate_obstacles(obstacle_clearance_m)
        else:
            print("No relevant features found to rasterize.")

    except Exception as e:
        print(f"Error fetching or processing OSM features: {e}")
        import traceback
        traceback.print_exc()
    
    start_utm_e_abs, start_utm_n_abs, _, _ = utm.from_latlon(start_lat, start_lon, force_zone_number=zone_num, force_zone_letter=zone_letter)
    goal_utm_e_abs, goal_utm_n_abs, _, _ = utm.from_latlon(goal_lat, goal_lon, force_zone_number=zone_num, force_zone_letter=zone_letter)

    start_grid_x, start_grid_y = grid_map.utm_to_grid_coords(start_utm_e_abs, start_utm_n_abs)
    goal_grid_x, goal_grid_y = grid_map.utm_to_grid_coords(goal_utm_e_abs, goal_utm_n_abs)
    
    print(f"Start Grid Coords: ({start_grid_x}, {start_grid_y}) for A*")
    print(f"Goal Grid Coords: ({goal_grid_x}, {goal_grid_y}) for A*")

    astar_path_grid = a_star_search(grid_map, (start_grid_x, start_grid_y), (goal_grid_x, goal_grid_y))

    map_center_folium = [ (start_lat + goal_lat) / 2, (start_lon + goal_lon) / 2 ]
    m = folium.Map(location=map_center_folium, zoom_start=19, tiles="OpenStreetMap") # Zoom 레벨 약간 더 높임

    folium.Marker(location=[start_lat, start_lon], popup="Start", icon=folium.Icon(color='green', icon='play')).add_to(m)
    folium.Marker(location=[goal_lat, goal_lon], popup="Goal", icon=folium.Icon(color='red', icon='stop')).add_to(m)

    # 원본 OSM 장애물 영역 (WGS84 좌표계 사용)
    if 'features_gdf_wgs84' in locals() and not features_gdf_wgs84.empty and 'geometry' in features_gdf_wgs84.columns:
        tooltip_candidate_fields = ['name', 'building', 'leisure', 'landuse', 'natural', 'amenity', 'barrier', 'power', 'man_made']
        available_tooltip_fields = [field for field in tooltip_candidate_fields if field in features_gdf_wgs84.columns]
        tooltip_obj = None
        if available_tooltip_fields:
            tooltip_obj = folium.features.GeoJsonTooltip(fields=available_tooltip_fields, aliases=None, localize=True, sticky=False, max_width=200)

        folium.GeoJson(
            features_gdf_wgs84[features_gdf_wgs84.is_valid & (~features_gdf_wgs84.is_empty)],
            name='OSM Obstacles (Original)',
            style_function=lambda x: {'fillColor': 'black', 'color': 'gray', 'weight': 1, 'fillOpacity': 0.3}, # 원본은 약간 연하게
            tooltip=tooltip_obj
        ).add_to(m)
    
    # (선택적 디버깅) 확장된 장애물 그리드를 지도에 표시 (UTM -> LatLon 변환 필요, 많은 셀이면 느릴 수 있음)
    # for r_idx in range(grid_map.grid_height):
    #     for c_idx in range(grid_map.grid_width):
    #         if grid_map.data[r_idx, c_idx] == 1: # 확장된 장애물 셀
    #             cell_e, cell_n = grid_map.grid_coords_to_utm(c_idx, r_idx)
    #             cell_lat, cell_lon = utm.to_latlon(cell_e, cell_n, grid_map.zone_number, grid_map.zone_letter)[:2]
    #             # folium.Rectangle(bounds=[...], color='red', fill_opacity=0.1).add_to(m) # 셀을 사각형으로 표시
    #             folium.CircleMarker(location=[cell_lat, cell_lon], radius=grid_map.resolution*0.5, color='red', fill=True, fill_color='red', fill_opacity=0.1).add_to(m)


    if astar_path_grid:
        astar_path_latlon = []
        for gx, gy in astar_path_grid:
            utm_e, utm_n = grid_map.grid_coords_to_utm(gx, gy)
            lat, lon = utm.to_latlon(utm_e, utm_n, grid_map.zone_number, grid_map.zone_letter)[:2]
            astar_path_latlon.append((lat, lon))
        
        folium.PolyLine(locations=astar_path_latlon, color='purple', weight=5, opacity=0.8, tooltip="A* Path (Inflated Grid)").add_to(m)
        print(f"A* path with {len(astar_path_latlon)} waypoints generated (after inflation).")
    else:
        print("No A* path found (possibly due to inflated obstacles or disconnected start/goal).")

    folium.LayerControl().add_to(m)
    m.save(output_html_filename)
    print(f"Map saved to {output_html_filename}. Open this file in a web browser.")
