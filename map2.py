import utm
import math
import heapq # A* 알고리즘의 우선순위 큐를 위해 사용
import numpy as np
import folium

# --- 1. 좌표 변환 및 그리드 설정 도우미 함수 ---

def latlon_to_utm(lat, lon):
    """위도, 경도를 UTM 좌표로 변환"""
    return utm.from_latlon(lat, lon)[:2] # easting, northing만 반환

def utm_to_latlon(easting, northing, zone_number, zone_letter):
    """UTM 좌표를 위도, 경도로 변환"""
    return utm.to_latlon(easting, northing, zone_number, zone_letter)[:2] # lat, lon만 반환

class GridMap:
    def __init__(self, width_m, height_m, resolution_m, origin_utm_e, origin_utm_n, origin_zone_num, origin_zone_letter):
        self.width_m = width_m
        self.height_m = height_m
        self.resolution = resolution_m  # 각 셀의 크기 (미터)
        self.origin_e = origin_utm_e    # 그리드 원점의 UTM Easting
        self.origin_n = origin_utm_n    # 그리드 원점의 UTM Northing
        self.zone_number = origin_zone_num
        self.zone_letter = origin_zone_letter

        self.grid_width = int(math.ceil(width_m / resolution_m))
        self.grid_height = int(math.ceil(height_m / resolution_m))
        
        # 그리드 초기화 (0: 통행 가능, 1: 장애물)
        self.data = np.zeros((self.grid_height, self.grid_width), dtype=np.uint8)
        print(f"Grid created: {self.grid_width}x{self.grid_height} cells, resolution: {self.resolution}m")

    def utm_to_grid_coords(self, utm_e, utm_n):
        """UTM 좌표를 그리드 인덱스 (x, y)로 변환"""
        grid_x = int((utm_e - self.origin_e) / self.resolution)
        grid_y = int((utm_n - self.origin_n) / self.resolution) # UTM 북쪽이 그리드 Y축 위쪽으로 매핑되도록
        return grid_x, grid_y

    def grid_coords_to_utm(self, grid_x, grid_y):
        """그리드 인덱스를 해당 셀 중심의 UTM 좌표로 변환"""
        utm_e = self.origin_e + (grid_x + 0.5) * self.resolution
        utm_n = self.origin_n + (grid_y + 0.5) * self.resolution
        return utm_e, utm_n

    def is_valid_grid_coords(self, grid_x, grid_y):
        """그리드 좌표가 유효한 범위 내에 있는지 확인"""
        return 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height

    def set_obstacle_rect_utm(self, min_e, min_n, max_e, max_n):
        """UTM 좌표 사각형 영역을 장애물로 설정"""
        start_gx, start_gy = self.utm_to_grid_coords(min_e, min_n)
        end_gx, end_gy = self.utm_to_grid_coords(max_e, max_n)

        # 그리드 좌표가 유효한 범위 내에 있도록 클리핑
        start_gx = max(0, min(start_gx, self.grid_width - 1))
        start_gy = max(0, min(start_gy, self.grid_height - 1))
        end_gx = max(0, min(end_gx, self.grid_width - 1))
        end_gy = max(0, min(end_gy, self.grid_height - 1))
        
        if start_gx > end_gx or start_gy > end_gy:
            print(f"Warning: Invalid obstacle rectangle UTM to Grid conversion. Min/Max swapped? ({start_gx},{start_gy}) to ({end_gx},{end_gy})")
            return

        self.data[start_gy:end_gy+1, start_gx:end_gx+1] = 1 # 장애물로 표시
        print(f"Obstacle rectangle set: grid cells ({start_gx},{start_gy}) to ({end_gx},{end_gy})")

    def set_obstacle_polygon_utm(self, polygon_utm_vertices):
        """UTM 좌표 다각형 영역을 장애물로 설정 (간단한 래스터화)"""
        # 다각형을 포함하는 최소 경계 사각형(MBR) 내의 모든 그리드 셀에 대해
        # 해당 셀의 중심이 다각형 내부에 있는지 검사 (Ray Casting 알고리즘 등 사용)
        # 여기서는 간단하게 경계 사각형만 장애물로 설정하거나, 더 정교한 라이브러리(shapely, OpenCV 등) 필요
        if not polygon_utm_vertices: return
        
        min_e = min(v[0] for v in polygon_utm_vertices)
        max_e = max(v[0] for v in polygon_utm_vertices)
        min_n = min(v[1] for v in polygon_utm_vertices)
        max_n = max(v[1] for v in polygon_utm_vertices)
        
        # MBR을 장애물로 설정 (단순화된 버전)
        # 더 정확하려면 각 셀이 폴리곤 내부에 있는지 point-in-polygon 테스트 필요
        print(f"Warning: Obstacle polygon set using its MBR for simplicity.")
        self.set_obstacle_rect_utm(min_e, min_n, max_e, max_n)


# --- 2. A* 알고리즘 구현 ---
def heuristic(a, b):
    """A* 휴리스틱 함수 (맨해튼 거리 또는 유클리드 거리)"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) # 맨해튼 거리
    # return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2) # 유클리드 거리

def a_star_search(grid_map, start_grid, goal_grid):
    """A* 경로 탐색 알고리즘"""
    if not grid_map.is_valid_grid_coords(start_grid[0], start_grid[1]) or \
       not grid_map.is_valid_grid_coords(goal_grid[0], goal_grid[1]):
        print("Error: Start or Goal grid coordinates are out of bounds.")
        return None
    if grid_map.data[start_grid[1], start_grid[0]] == 1 or \
       grid_map.data[goal_grid[1], goal_grid[0]] == 1:
        print("Error: Start or Goal is on an obstacle.")
        return None

    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), # 상하좌우
                 (1, 1), (1, -1), (-1, 1), (-1, -1)] # 대각선 (대각선 이동 비용 고려 필요)

    open_set = []
    heapq.heappush(open_set, (0, start_grid)) # (f_cost, (x, y))

    came_from = {} # 경로 추적용: node -> parent_node
    g_score = {start_grid: 0} # 시작점으로부터의 실제 비용
    f_score = {start_grid: heuristic(start_grid, goal_grid)} # 총 예상 비용 (g + h)

    path_found_count = 0 # 디버깅용

    while open_set:
        current_f_score, current_node = heapq.heappop(open_set)
        path_found_count +=1

        if current_node == goal_grid:
            print(f"A* path found! Explored {path_found_count} nodes.")
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start_grid) # 시작점 추가
            return path[::-1] # 역순으로 반환

        for dx, dy in neighbors:
            neighbor_node = (current_node[0] + dx, current_node[1] + dy)

            if not grid_map.is_valid_grid_coords(neighbor_node[0], neighbor_node[1]) or \
               grid_map.data[neighbor_node[1], neighbor_node[0]] == 1: # 장애물이거나 맵 밖이면 건너뜀
                continue
            
            # 이동 비용 (상하좌우는 1, 대각선은 sqrt(2) ~ 1.414)
            move_cost = 1.414 if abs(dx) == 1 and abs(dy) == 1 else 1.0
            tentative_g_score = g_score[current_node] + move_cost

            if neighbor_node not in g_score or tentative_g_score < g_score[neighbor_node]:
                came_from[neighbor_node] = current_node
                g_score[neighbor_node] = tentative_g_score
                f_score[neighbor_node] = tentative_g_score + heuristic(neighbor_node, goal_grid)
                if not any(item[1] == neighbor_node for item in open_set): # open_set에 없으면 추가
                     heapq.heappush(open_set, (f_score[neighbor_node], neighbor_node))
    
    print(f"A* failed to find a path after exploring {path_found_count} nodes.")
    return None


# --- 3. 메인 실행 부분 ---
if __name__ == '__main__':
    # --- 사용자 설정 영역 ---
    # 예시: 여수 제1공학관(F16) 근처 영역
    # 실제 환경에 맞게 출발지, 목적지, 장애물 영역, 그리드 설정을 정확히 입력해야 합니다.

    # (A) 출발지 및 목적지 좌표 (위도, 경도)
    start_lat, start_lon = 34.776718, 127.700792  # 예시: 제1공학관 남쪽
    goal_lat, goal_lon = 34.776691, 127.700290    # 예시: 제1공학관 북동쪽

    # (B) 그리드 맵 설정
    # 그리드 원점: 출발지/목적지를 포함하는 영역의 좌하단 UTM 좌표를 사용하는 것이 편리
    # 임시로 출발지를 원점 근처로 하고, 영역 크기를 설정
    temp_origin_e, temp_origin_n, zone_num, zone_letter = utm.from_latlon(start_lat, start_lon)
    
    grid_origin_e = temp_origin_e - 50   # 출발지에서 서쪽으로 50m
    grid_origin_n = temp_origin_n - 50   # 출발지에서 남쪽으로 50m
    map_width_m = 200                   # 맵의 전체 폭 (미터)
    map_height_m = 200                  # 맵의 전체 높이 (미터)
    grid_resolution = 0.5               # 그리드 해상도 (셀 하나당 미터) - 작을수록 정교하지만 계산량 증가

    grid_map = GridMap(map_width_m, map_height_m, grid_resolution, 
                       grid_origin_e, grid_origin_n, zone_num, zone_letter)

    # (C) 장애물 영역 정의 (UTM 좌표 기준) - 실제 환경에 맞게 여러 개 정의 가능
    # 예시: F16 건물 (실제 좌표로 대체 필요)
    # (min_easting, min_northing, max_easting, max_northing)
    # 이 좌표들은 grid_origin_e, grid_origin_n 기준으로 상대적인 값이 아니라 절대 UTM 값이어야 합니다.
    # (위도, 경도) -> UTM 변환 후 사용
    f16_sw_lat, f16_sw_lon = 34.7608, 127.6772 # F16 남서쪽 모서리 (예시)
    f16_ne_lat, f16_ne_lon = 34.7612, 127.6778 # F16 북동쪽 모서리 (예시)
    f16_min_e, f16_min_n = latlon_to_utm(f16_sw_lat, f16_sw_lon)
    f16_max_e, f16_max_n = latlon_to_utm(f16_ne_lat, f16_ne_lon)
    grid_map.set_obstacle_rect_utm(f16_min_e, f16_min_n, f16_max_e, f16_max_n)

    # 예시: 정원 영역 (실제 좌표로 대체 필요)
    garden_sw_lat, garden_sw_lon = 34.7613, 127.6775 # 정원 남서쪽 (예시)
    garden_ne_lat, garden_ne_lon = 34.7616, 127.6780 # 정원 북동쪽 (예시)
    garden_min_e, garden_min_n = latlon_to_utm(garden_sw_lat, garden_sw_lon)
    garden_max_e, garden_max_n = latlon_to_utm(garden_ne_lat, garden_ne_lon)
    grid_map.set_obstacle_rect_utm(garden_min_e, garden_min_n, garden_max_e, garden_max_n)
    
    # --- 경로 탐색 ---
    start_utm_e, start_utm_n = latlon_to_utm(start_lat, start_lon)
    goal_utm_e, goal_utm_n = latlon_to_utm(goal_lat, goal_lon)

    start_grid_x, start_grid_y = grid_map.utm_to_grid_coords(start_utm_e, start_utm_n)
    goal_grid_x, goal_grid_y = grid_map.utm_to_grid_coords(goal_utm_e, goal_utm_n)

    print(f"Start UTM: ({start_utm_e:.2f}, {start_utm_n:.2f}) -> Grid: ({start_grid_x}, {start_grid_y})")
    print(f"Goal UTM: ({goal_utm_e:.2f}, {goal_utm_n:.2f}) -> Grid: ({goal_grid_x}, {goal_grid_y})")

    astar_path_grid = a_star_search(grid_map, (start_grid_x, start_grid_y), (goal_grid_x, goal_grid_y))

    # --- 결과 시각화 ---
    map_center_lat = (start_lat + goal_lat) / 2
    map_center_lon = (start_lon + goal_lon) / 2
    m = folium.Map(location=[map_center_lat, map_center_lon], zoom_start=18, tiles="OpenStreetMap")

    # 출발지, 목적지 마커
    folium.Marker(location=[start_lat, start_lon], popup="Start", icon=folium.Icon(color='green', icon='play')).add_to(m)
    folium.Marker(location=[goal_lat, goal_lon], popup="Goal", icon=folium.Icon(color='red', icon='stop')).add_to(m)

    # 장애물 영역 표시 (UTM -> LatLon 변환하여 Folium에 추가)
    # F16 건물
    f16_poly_latlon = [
        utm_to_latlon(f16_min_e, f16_min_n, zone_num, zone_letter),
        utm_to_latlon(f16_max_e, f16_min_n, zone_num, zone_letter),
        utm_to_latlon(f16_max_e, f16_max_n, zone_num, zone_letter),
        utm_to_latlon(f16_min_e, f16_max_n, zone_num, zone_letter),
        utm_to_latlon(f16_min_e, f16_min_n, zone_num, zone_letter) # 닫힌 폴리곤
    ]
    folium.Polygon(locations=f16_poly_latlon, color='black', fill=True, fill_color='black', fill_opacity=0.4, tooltip="Building F16 (Obstacle)").add_to(m)
    
    # 정원
    garden_poly_latlon = [
        utm_to_latlon(garden_min_e, garden_min_n, zone_num, zone_letter),
        utm_to_latlon(garden_max_e, garden_min_n, zone_num, zone_letter),
        utm_to_latlon(garden_max_e, garden_max_n, zone_num, zone_letter),
        utm_to_latlon(garden_min_e, garden_max_n, zone_num, zone_letter),
        utm_to_latlon(garden_min_e, garden_min_n, zone_num, zone_letter)
    ]
    folium.Polygon(locations=garden_poly_latlon, color='darkgreen', fill=True, fill_color='green', fill_opacity=0.4, tooltip="Garden (Obstacle)").add_to(m)


    if astar_path_grid:
        # 그리드 경로를 UTM 좌표로 변환 후, 다시 위도/경도로 변환
        astar_path_latlon = []
        for gx, gy in astar_path_grid:
            utm_e, utm_n = grid_map.grid_coords_to_utm(gx, gy)
            lat, lon = utm_to_latlon(utm_e, utm_n, grid_map.zone_number, grid_map.zone_letter)
            astar_path_latlon.append((lat, lon))
        
        folium.PolyLine(locations=astar_path_latlon, color='purple', weight=5, opacity=0.8, tooltip="A* Path").add_to(m)
        print(f"A* path with {len(astar_path_latlon)} waypoints generated.")

        # 로봇이 사용할 UTM 웨이포인트 (필요시 출력)
        # astar_path_utm = [grid_map.grid_coords_to_utm(gx, gy) for gx, gy in astar_path_grid]
        # print("A* Path (UTM):", astar_path_utm)

    else:
        print("No path found by A* algorithm.")

    output_filename = "astar_path_visualization.html"
    m.save(output_filename)
    print(f"Map saved to {output_filename}")
