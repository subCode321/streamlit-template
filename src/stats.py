import streamlit as st
import psutil
import time

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    memory = psutil.virtual_memory()
    return memory.percent


