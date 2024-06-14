import os
from typing import List
from fastapi import UploadFile, Depends

from app.models.user import User
from app.utils.authorize import authorize


class PictureService:
    def __init__(self):
        pass

    async def upload_picture(self, files: List[UploadFile]):
        try:
            upload_folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/uploaded_files'
            os.makedirs(upload_folder, exist_ok=True)
            for file in files:
                with open(upload_folder + f'/{file.filename}', 'wb+') as f:
                    f.write(await file.read())
            # return {"filename": file.filename}
        except Exception as e:
            return {"error": str(e)}

    def match_key_points(self):
        import cv2
        import numpy as np
        import tkinter as tk
        from itertools import combinations
        import math

        def detect_keypoints_and_descriptors(image_path):
            try:
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                if image is None:
                    raise ValueError(f"图像读取失败，请检查文件路径：{image_path}")

                sift = cv2.SIFT_create()
                keypoints, descriptors = sift.detectAndCompute(image, None)
                return keypoints, descriptors, image.shape
            except Exception as e:
                print(e)
                return None, None, None

        def divide_image(image_shape, num_regions):
            h, w = image_shape
            region_height = h // num_regions
            region_width = w // num_regions
            regions = [(i * region_height, (i + 1) * region_height, j * region_width, (j + 1) * region_width)
                       for i in range(num_regions) for j in range(num_regions)]
            return regions

        def select_spread_out_points(matches, keypoints1, keypoints2, image_shape1, num_regions=3):
            if len(matches) <= num_regions:
                return matches

            regions = divide_image(image_shape1, num_regions)
            region_matches = [[] for _ in range(len(regions))]

            for m in matches:
                x1, y1 = keypoints1[m.queryIdx].pt
                for i, (y0, y1_, x0, x1_) in enumerate(regions):
                    if y0 <= y1 < y1_ and x0 <= x1 < x1_:
                        region_matches[i].append(m)
                        break

            spread_out_matches = []
            for region in region_matches:
                if region:
                    spread_out_matches.append(min(region, key=lambda m: m.distance))

            if len(spread_out_matches) > num_regions:
                spread_out_matches = spread_out_matches[:num_regions]

            return spread_out_matches

        def calculate_angle(a, b, c):
            """计算三角形ABC的角度"""
            ab = np.linalg.norm(a - b)
            bc = np.linalg.norm(b - c)
            ca = np.linalg.norm(c - a)
            angle_b = np.arccos((ab ** 2 + bc ** 2 - ca ** 2) / (2 * ab * bc))
            return np.degrees(angle_b)

        def is_acute_triangle(a, b, c):
            angle_a = calculate_angle(b, c, a)
            angle_b = calculate_angle(c, a, b)
            angle_c = calculate_angle(a, b, c)
            return angle_a < 90 and angle_b < 90 and angle_c < 90

        def is_almost_equilateral(a, b, c, tolerance=0.05):
            """判断三角形是否近似等边"""
            ab = np.linalg.norm(a - b)
            bc = np.linalg.norm(b - c)
            ca = np.linalg.norm(c - a)
            max_len = max(ab, bc, ca)
            min_len = min(ab, bc, ca)
            return (max_len - min_len) / max_len < tolerance

        def is_almost_collinear(a, b, c, tolerance=1e-2):
            """判断三点是否近似共线"""
            area = 0.5 * np.abs(a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
            return area < tolerance

        def select_triangle_points(matches, keypoints1, image_shape1, num_regions=3):
            spread_out_matches = select_spread_out_points(matches, keypoints1, keypoints1, image_shape1, num_regions)
            keypoints = [keypoints1[m.queryIdx].pt for m in spread_out_matches]
            for comb in combinations(keypoints, 3):
                a, b, c = np.array(comb[0]), np.array(comb[1]), np.array(comb[2])
                if is_acute_triangle(a, b, c) and not is_almost_equilateral(a, b, c) and not is_almost_collinear(a, b,
                                                                                                                 c):
                    return [spread_out_matches[keypoints.index(pt)] for pt in comb]
            return spread_out_matches

        def match_keypoints(keypoints1, keypoints2, descriptors1, descriptors2, image_shape1, ratio=0.7,
                            ransac_thresh=5.0):
            index_params = dict(algorithm=1, trees=5)
            search_params = dict(checks=50)
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(descriptors1, descriptors2, k=2)

            good_matches = []
            for m, n in matches:
                if m.distance < ratio * n.distance:
                    good_matches.append(m)

            if not good_matches:
                print("没有找到好的匹配点。")
                return []

            src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            _, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, ransac_thresh)

            matches_mask = mask.ravel().tolist()
            good_matches = [m for m, mask in zip(good_matches, matches_mask) if mask]

            # 选择满足条件的三角形特征点
            selected_matches = select_triangle_points(good_matches, keypoints1, image_shape1)

            return selected_matches

        # def draw_matches(image_path1, image_path2, keypoints1, keypoints2, matches):
        #     try:
        #         image1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
        #         image2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)
        #         if image1 is None or image2 is None:
        #             raise ValueError("图像读取失败，请检查文件路径。")
        #
        #         matched_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches, None,
        #                                         flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        #
        #         root = tk.Tk()
        #         screen_width = root.winfo_screenwidth()
        #         screen_height = root.winfo_screenheight()
        #         root.withdraw()
        #
        #         scale_width = screen_width / matched_image.shape[1]
        #         scale_height = screen_height / matched_image.shape[0]
        #         scale = min(scale_width, scale_height)
        #
        #         window_width = int(matched_image.shape[1] * scale)
        #         window_height = int(matched_image.shape[0] * scale)
        #         resized_image = cv2.resize(matched_image, (window_width, window_height))
        #
        #         for match in matches:
        #             img1_idx = match.queryIdx
        #             img2_idx = match.trainIdx
        #             (x1, y1) = keypoints1[img1_idx].pt
        #             (x2, y2) = keypoints2[img2_idx].pt
        #             x2 += image1.shape[1]
        #
        #             cv2.circle(resized_image, (int(x1 * scale), int(y1 * scale)), 10, (0, 255, 0), 2)
        #             cv2.circle(resized_image, (int(x2 * scale), int(y2 * scale)), 10, (0, 0, 255), 2)
        #             cv2.line(resized_image, (int(x1 * scale), int(y1 * scale)), (int(x2 * scale), int(y2 * scale)), (255, 0, 0), 2)
        #
        #         cv2.imshow('匹配关键点', resized_image)
        #         cv2.waitKey(0)
        #         cv2.destroyAllWindows()
        #     except Exception as e:
        #         print(e)

        # # 图像路径
        # image_path1 = 'book1.jpg'
        # image_path2 = 'book2.jpg'
        import os

        # 设置uploaded_files目录路径
        uploaded_files_dir = 'uploaded_files'

        # 获取uploaded_files目录下的所有文件
        all_files = os.listdir(uploaded_files_dir)

        # 筛选出以1.jpg或2.jpg结尾的文件
        files_to_read = [f for f in all_files if f.endswith(('1.jpg', '2.jpg'))]

        # 按照某种逻辑（例如文件名的顺序）分别赋值给image_path1和image_path2
        # 假设我们按照文件名的字典顺序来分配
        files_to_read.sort()

        # 检查是否找到两个文件
        if len(files_to_read) >= 2:
            image_path1 = os.path.join(uploaded_files_dir, files_to_read[0])
            image_path2 = os.path.join(uploaded_files_dir, files_to_read[1])
        else:
            print("未找到足够的文件。")
            image_path1 = None
            image_path2 = None

        # 现在你可以使用image_path1和image_path2来读取文件
        if image_path1 and image_path2:
            # 使用Pillow库读取图像
            from PIL import Image
            image1 = Image.open(image_path1)
            image2 = Image.open(image_path2)
            # 这里可以添加对图像的进一步处理
            print(f"读取了文件: {image_path1}")
            print(f"读取了文件: {image_path2}")
        else:
            print("无法读取文件。")

        # 检测关键点和描述子
        keypoints1, descriptors1, image_shape1 = detect_keypoints_and_descriptors(image_path1)
        keypoints2, descriptors2, image_shape2 = detect_keypoints_and_descriptors(image_path2)

        # 检查是否成功检测到描述子
        if descriptors1 is not None and descriptors2 is not None:
            # 匹配关键点
            matches = match_keypoints(keypoints1, keypoints2, descriptors1, descriptors2, image_shape1)

            # 打印匹配点坐标
            if matches:
                for match in matches:
                    img1_idx = match.queryIdx
                    img2_idx = match.trainIdx
                    (x1, y1) = keypoints1[img1_idx].pt
                    (x2, y2) = keypoints2[img2_idx].pt
                    print(f"图像1 - 关键点: ({x1}, {y1})")
                    print(f"图像2 - 关键点: ({x2}, {y2})")
            else:
                print("没有找到足够的匹配点。")

            # # 显示匹配结果
            # draw_matches(image_path1, image_path2, keypoints1, keypoints2, matches)
        else:
            print("关键点或描述子检测失败。")


        return
