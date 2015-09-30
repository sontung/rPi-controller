import argparse
import sys

print sys.argv
parser = argparse.ArgumentParser()
parser.add_argument("light on")
args = parser.parse_args()