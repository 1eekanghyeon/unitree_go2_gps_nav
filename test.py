#!/usr/bin/env python3
import requests

def get_osrm_waypoints(current_lat, current_lon, goal_lat, goal_lon):
    """
    OSRM public API를 호출해서 'foot' 모드로 경로를 받아옵니다.
    반환값은 [(lat, lon), ...] 형태의 리스트입니다.
    """
    # OSRM 서버 URL
    url = f"http://router.project-osrm.org/route/v1/foot/{current_lon},{current_lat};{goal_lon},{goal_lat}"
    params = {
        'overview': 'full',      # 전체 경로를 GeoJSON 형식으로
        'geometries': 'geojson'
    }
    resp = requests.get(url, params=params, timeout=5.0)
    resp.raise_for_status()
    data = resp.json()

    # 첫 번째 경로(routes[0])의 geometry.coordinates를 가져옵니다.
    # OSRM은 [lon, lat] 쌍을 반환하므로, (lat, lon)으로 변환합니다.
    coords = data['routes'][0]['geometry']['coordinates']
    waypoints = [(lat, lon) for lon, lat in coords]
    return waypoints

if __name__ == '__main__':
    # ─── 이 부분만 바꿔 주세요 ────────────────────────────────────
    current_lat = 34.776579    # 예: 현재 위도
    current_lon = 127.701285   # 예: 현재 경도
    goal_lat = 34.776368       # 예: 목표 위도
    goal_lon = 127.699896      # 예: 목표 경도
    # ────────────────────────────────────────────────────────────

    waypoints = get_osrm_waypoints(current_lat, current_lon, goal_lat, goal_lon)
    print(f"총 {len(waypoints)}개의 waypoint를 받았습니다:")
    for idx, (lat, lon) in enumerate(waypoints):
        print(f"  {idx:3d}: lat={lat:.6f}, lon={lon:.6f}")
