from hh_analysis.pipelines.extract_areas import main as extract_areas
from hh_analysis.pipelines.transform_areas import main as transform_areas
from hh_analysis.pipelines.load_areas import main as load_areas


def main():
    extract_areas()
    transform_areas()
    load_areas()

if __name__ == '__main__':
    main()