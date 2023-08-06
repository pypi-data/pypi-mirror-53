#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pichi.utils import get_options


def main() -> None:
    options = get_options()
    options['func']()


if __name__ == '__main__':
    main()
