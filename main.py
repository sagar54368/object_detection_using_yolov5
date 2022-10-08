from io import StringIO
from pathlib import Path
import streamlit as st
import time
from detect import detect
import os
import sys
import argparse
from PIL import Image


def get_subdirs(b='.'):
    '''
        Returns all sub-directories in a specific Path
    '''
    result = []
    for d in os.listdir(b):
        bd = os.path.join(b, d)
        if os.path.isdir(bd):
            result.append(bd)
    return result


def get_detection_folder():
    '''
        Returns the latest folder in a runs\detect
    '''
    return max(get_subdirs(os.path.join('runs', 'detect')), key=os.path.getmtime)


if __name__ == '__main__':

    col2, col3 = st.columns([6,1])
    st.title("Welcome to Streamlit app")
    st.write("You can view real-time object detection done using YOLO model here. Select one of the following options to proceed:")

    with col3:
        st.image('logo.png')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str,
                        default='weights/yolov5s.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str,
                        default='data/images', help='source')
    parser.add_argument('--img-size', type=int, default=640,
                        help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float,
                        default=0.35, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float,
                        default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='',
                        help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true',
                        help='display results')
    parser.add_argument('--save-txt', action='store_true',
                        help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true',
                        help='save confidences in --save-txt labels')
    parser.add_argument('--nosave', action='store_true',
                        help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int,
                        help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true',
                        help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true',
                        help='augmented inference')
    parser.add_argument('--update', action='store_true',
                        help='update all models')
    parser.add_argument('--project', default='runs/detect',
                        help='save results to project/name')
    parser.add_argument('--name', default='exp',
                        help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true',
                        help='existing project/name ok, do not increment')
    opt = parser.parse_args()
    print(opt)

    source = ["Image", "Video","Webcam"] 
    source_index = st.sidebar.radio("selectbox", range(
        len(source)), format_func=lambda x: source[x]) 

    if source_index == 0:
        uploaded_file = st.sidebar.file_uploader(
            "image", type=['png', 'jpeg', 'jpg'])

        if uploaded_file is None:
            with st.sidebar:
                st.header("Please upload an image file") 

        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='Loading...'): 
                st.sidebar.image(uploaded_file)
                picture = Image.open(uploaded_file)
                picture = picture.save(f'data/images/{uploaded_file.name}')
                opt.source = f'data/images/{uploaded_file.name}'
        else:
            is_valid = False

    elif source_index == 1:
        uploaded_file = st.sidebar.file_uploader("video", type=['mp4', 'mpeg', 'mov'])
        if uploaded_file is None:
            with st.sidebar:
                st.header("Please upload a video file")

        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='Loading...'): 
                st.sidebar.video(uploaded_file)
                with open(os.path.join("data", "videos", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                opt.source = f'data/videos/{uploaded_file.name}'
        else:
            is_valid = False

    else:
        is_valid = True
        opt.source = str(0) 
        opt.nosave = True

    col2, col3 = st.columns([6,1])

    if is_valid:
        print('valid')
        if st.button('Click Here To Start Detection'): # when the button is clicked

            detect(opt) 

            with col2:
                if source_index == 0:
                    with st.spinner(text='Preparing Images'):
                        for img in os.listdir(get_detection_folder()):
                            st.image(str(Path(f'{get_detection_folder()}') / img))

                        st.balloons()

                elif source_index == 1:
                    with st.spinner(text='Preparing Video'):
                        for vid in os.listdir(get_detection_folder()):
                            st.video(str(Path(f'{get_detection_folder()}') / vid))

                        st.balloons()
                        