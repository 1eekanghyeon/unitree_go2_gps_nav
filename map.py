import requests
import json
import utm
import math
from collections import deque # interpolate_latlon_path에서 사용되진 않지만, 원본 클래스에서 가져올 때 딸려올 수 있음
import folium # 지도 시각화를 위한 라이브러리

# --- 기존 OutdoorNavigationNode 클래스에서 필요한 함수들을 가져옵니다 ---
# (실제 클래스 정의 없이 함수만 사용하거나, 필요시 간단한 헬퍼 클래스로 묶을 수 있습니다)

OSRM_SERVER_ADDRESS = 'http://router.project-osrm.org' # OSRM 공개 서버
# OSRM_SERVER_ADDRESS = 'http://localhost:5000' # 로컬 OSRM 서버 사용 시

def get_osrm_route(start_latlon, end_latlon, profile="foot"): # 기본 프로파일을 "foot"으로 변경
    """OSRM 서버에 경로를 요청하고 위도/경도 좌표 목록을 반환합니다."""
    # OSRM은 경도, 위도 순서로 좌표를 받습니다.
    url = (f"{OSRM_SERVER_ADDRESS}/route/v1/{profile}/"
           f"{start_latlon[1]},{start_latlon[0]};{end_latlon[1]},{end_latlon[0]}"
           f"?overview=full&geometries=geojson&steps=false") # steps=true도 가능하나, 여기선 false로 단순화
    
    print(f"Requesting OSRM route: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        route_data = response.json()

        if route_data.get('routes') and route_data['routes'][0].get('geometry'):
            geometry = route_data['routes'][0]['geometry']['coordinates']
            # OSRM은 [경도, 위도] 순서로 주므로, folium 및 내부 사용을 위해 [위도, 경도]로 변경
            latlon_path = [[coord[1], coord[0]] for coord in geometry]
            print(f"OSRM route received with {len(latlon_path)} points.")
            return latlon_path
        else:
            print(f"OSRM Error: No route found or geometry missing. Response: {route_data.get('message', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"OSRM request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Failed to decode OSRM JSON response: {e}")
        return None

def interpolate_latlon_path(latlon_path, desired_distance_m):
    """위도/경도 경로를 일정한 거리 간격으로 보간합니다."""
    if not latlon_path or len(latlon_path) < 2 or desired_distance_m <= 0:
        print(f"Path interpolation skipped: path_len={len(latlon_path)}, desired_dist={desired_distance_m}")
        return latlon_path

    interpolated_path = [latlon_path[0]] 
    
    try:
        # 첫 번째 점의 UTM 존 정보를 기준으로 전체 경로 보간 (일관성 유지)
        # utm.from_latlon은 (easting, northing, zone_number, zone_letter) 반환
        _, _, base_zone_num, base_zone_let = utm.from_latlon(latlon_path[0][0], latlon_path[0][1])
    except Exception as e:
        print(f"Cannot get base UTM for interpolation start: {e}")
        return latlon_path # 오류 시 원본 경로 반환

    for i in range(len(latlon_path) - 1):
        start_lat, start_lon = latlon_path[i]
        end_lat, end_lon = latlon_path[i+1]

        # OSRM 경로에 동일 지점이 연속으로 나올 경우 건너뛰기
        if abs(start_lat - end_lat) < 1e-7 and abs(start_lon - end_lon) < 1e-7: # 1e-7 (약 0.01m 이내)
            continue

        try:
            start_e, start_n, _, _ = utm.from_latlon(start_lat, start_lon, force_zone_number=base_zone_num, force_zone_letter=base_zone_let)
            end_e, end_n, _, _ = utm.from_latlon(end_lat, end_lon, force_zone_number=base_zone_num, force_zone_letter=base_zone_let)
        except Exception as e:
            print(f"UTM conversion error in interpolation for segment {i} ([{start_lat},{start_lon}] -> [{end_lat},{end_lon}]): {e}")
            # 오류 발생 시, 이 세그먼트의 끝점을 이전 보간점과 다를 경우에만 추가 (중복 방지)
            if not interpolated_path or \
               (abs(interpolated_path[-1][0] - end_lat) > 1e-7 or abs(interpolated_path[-1][1] - end_lon) > 1e-7):
                interpolated_path.append([end_lat, end_lon])
            continue

        segment_dx = end_e - start_e
        segment_dy = end_n - start_n
        segment_length_m = math.hypot(segment_dx, segment_dy)

        if segment_length_m < 1e-3: # 1mm 이하 세그먼트는 거의 같은 점으로 간주, 끝점만 추가 (중복 방지)
            if not interpolated_path or \
               (abs(interpolated_path[-1][0] - end_lat) > 1e-7 or abs(interpolated_path[-1][1] - end_lon) > 1e-7):
                interpolated_path.append([end_lat, end_lon])
            continue
        
        num_intermediate_points = math.floor(segment_length_m / desired_distance_m)

        for j in range(1, int(num_intermediate_points) + 1):
            ratio = (j * desired_distance_m) / segment_length_m
            if ratio >= 0.999: # 거의 세그먼트 끝에 도달하면 루프 중단 (부동소수점 오차 감안)
                break 
            
            inter_e = start_e + ratio * segment_dx
            inter_n = start_n + ratio * segment_dy
            
            try:
                inter_lat, inter_lon = utm.to_latlon(inter_e, inter_n, base_zone_num, base_zone_let)
                # 이전 보간점과 매우 가까우면(거의 동일하면) 추가하지 않음
                if not interpolated_path or \
                   (abs(interpolated_path[-1][0] - inter_lat) > 1e-7 or abs(interpolated_path[-1][1] - inter_lon) > 1e-7):
                    interpolated_path.append([inter_lat, inter_lon])
            except Exception as e:
                print(f"UTM to LatLon conversion error for interpolated point ({inter_e}, {inter_n}): {e}")
        
        # 각 OSRM 세그먼트의 끝점은 항상 포함 (중복 방지)
        if not interpolated_path or \
           (abs(interpolated_path[-1][0] - end_lat) > 1e-7 or abs(interpolated_path[-1][1] - end_lon) > 1e-7):
            interpolated_path.append([end_lat, end_lon])
    
    print(f"Interpolated OSRM path to {len(interpolated_path)} lat/lon waypoints.")
    return interpolated_path

# --- 메인 실행 부분 ---
if __name__ == '__main__':
    # 1. 출발지 및 목적지 좌표 설정 (예: 여수 이순신광장 -> 여수엑스포역)
    # 실제 사용 시에는 이 부분을 사용자 입력이나 다른 방식으로 받아오도록 수정 가능
    start_latitude = 34.776700  # 이순신광장 근처 위도
    start_longitude = 127.700803 # 이순신광장 근처 경도
    
    end_latitude = 34.776742    # 여수엑스포역 근처 위도
    end_longitude = 127.700336  # 여수엑스포역 근처 경도

    start_coords = (start_latitude, start_longitude)
    end_coords = (end_latitude, end_longitude)

    # 2. OSRM 프로파일 선택 ('driving', 'foot', 'bicycle')
    # 로봇의 이동 특성에 맞는 프로파일을 선택하세요. "도보"의 경우 "foot"을 사용합니다.
    osrm_profile = "foot" # <--- 여기서 프로파일을 변경하며 테스트 가능
    print(f"Using OSRM profile: {osrm_profile}")

    # 3. OSRM을 통해 경로 받아오기
    raw_osrm_waypoints = get_osrm_route(start_coords, end_coords, profile=osrm_profile)

    if raw_osrm_waypoints:
        print(f"Successfully fetched {len(raw_osrm_waypoints)} raw OSRM waypoints.")

        # 4. (선택 사항) 경로 보간
        interpolation_distance = 0.5 # 보간 간격 (미터), OutdoorNavigationNode와 동일하게 설정하여 비교
        interpolated_waypoints = interpolate_latlon_path(raw_osrm_waypoints, interpolation_distance)
        print(f"Interpolated path to {len(interpolated_waypoints)} waypoints with {interpolation_distance}m interval.")

        # 5. Folium을 사용하여 지도에 시각화
        # 지도의 초기 중심점을 출발지와 목적지의 중간 정도로 설정
        map_center_lat = (start_coords[0] + end_coords[0]) / 2
        map_center_lon = (start_coords[1] + end_coords[1]) / 2
        
        # Folium 지도 객체 생성
        # 다양한 타일 사용 가능: 'OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'CartoDB positron' 등
        m = folium.Map(location=[map_center_lat, map_center_lon], zoom_start=15, tiles="OpenStreetMap")

        # 출발지 마커 추가
        folium.Marker(
            location=[start_coords[0], start_coords[1]],
            popup="Start Point",
            icon=folium.Icon(color="green", icon="play")
        ).add_to(m)

        # 목적지 마커 추가
        folium.Marker(
            location=[end_coords[0], end_coords[1]],
            popup="End Point",
            icon=folium.Icon(color="red", icon="stop")
        ).add_to(m)

        # OSRM 원본 경로 그리기
        if raw_osrm_waypoints:
            folium.PolyLine(
                locations=raw_osrm_waypoints,
                color="blue",
                weight=5,
                opacity=0.7,
                tooltip="Raw OSRM Route"
            ).add_to(m)

        # 보간된 경로 그리기
        if interpolated_waypoints and len(interpolated_waypoints) > 1 : # 경로점이 2개 이상일 때만 그림
            folium.PolyLine(
                locations=interpolated_waypoints,
                color="orange",
                weight=3,
                opacity=0.9,
                tooltip=f"Interpolated Route ({interpolation_distance}m)"
            ).add_to(m)
            # 보간된 웨이포인트에 작은 원 마커 표시 (너무 많으면 지저분해질 수 있으므로 선택적)
            # for point in interpolated_waypoints:
            #     folium.CircleMarker(location=point, radius=1, color='red', fill=True, fill_color='darkred').add_to(m)


        # 생성된 지도를 HTML 파일로 저장
        output_filename = f"osrm_route_visualization_{osrm_profile}.html"
        m.save(output_filename)
        print(f"Map saved to {output_filename}")
        print(f"Open this file in a web browser to view the route.")

    else:
        print("Could not retrieve route from OSRM.")
