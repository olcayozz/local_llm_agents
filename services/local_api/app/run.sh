#!/bin/bash
uvicorn main:app --host 0.0.0.0 --port 5000 --reload;
tail -F anything;