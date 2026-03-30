"""Transform HH areas tree into flat records."""

def flatten_areas(areas: list) -> list:
    """Convert HH areas tree to flat table."""

    result = []

    def walk(area, parent_id=None, level=0):
        result.append(
            {
                "area_id": int(area["id"]),
                "parent_area_id": int(parent_id) if parent_id else None,
                "area_name": area["name"],
                "level": level,
            }
        )

        for child in area.get("areas", []):
            walk(child, area["id"], level + 1)

    for root in areas:
        walk(root)

    return result
