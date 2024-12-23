#!/bin/sh
./api_parse.jq|sort -u|./parse_print.jq|sort
