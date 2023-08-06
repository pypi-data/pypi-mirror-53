"""
Main entrypoint for ocupgrader.
"""

from ocdeployer.utils import oc

def main():
    project = oc("project", "-q").strip()
    print(project)

if __name__ == "__main__":
    main()
