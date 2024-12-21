from shapely import wkt  
def parse_wkt_to_coordinates(wkt_str: str):
    """ Fungsi untuk mengonversi WKT (Well Known Text) ke list koordinat """
    print(f"Parsing WKT: {wkt_str}")  # Pastikan ini adalah string WKT yang valid
    polygon = wkt.loads(wkt_str)  # Parsing WKT menjadi objek Polygon
    coordinates = list(polygon.exterior.coords)  # Mengembalikan koordinat sebagai list
    print(f"Parsed coordinates: {coordinates}")
    return coordinates