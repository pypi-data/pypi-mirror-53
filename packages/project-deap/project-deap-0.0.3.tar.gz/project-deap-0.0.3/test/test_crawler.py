from deap import crawler
import subprocess as sub


def test_crawler():
    sub.call(['python3', '../deap/crawler.py'])

    sub.call(['python3', '../deap/crawler.py', '--extension', 'py'])


