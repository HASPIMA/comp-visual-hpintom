# Manual vs OpenCV convolution
In the manual convolution, the image is first padded with zeros to handle borders. A kernel is then slid over each pixel of the image, performing element-wise multiplication with the overlapping region. The sum of these products is written to the corresponding pixel in the output image. This process is repeated for every pixel, and values are clipped to the \[0, 255] range.

In contrast, OpenCV's `cv2.filter2D()` is highly optimized in C++ for performance, handles various padding strategies gracefully, and can leverage fast algorithms like FFT for large kernels. Our manual version is purely spatial and less efficient but fully transparent in its logic.

# Images
![1](https://github.com/user-attachments/assets/6a95ecc4-b62d-4cbb-b3a9-219fb9c39a78)
![2](https://github.com/user-attachments/assets/44faf50b-4d9a-431c-803e-6b93dc3ca7cd)

# Link
[Google Colab](https://colab.research.google.com/drive/1Fe6WFXN1Jn6b9n4k3Zq4mtwVLrazRBzC?usp=drive_link)

# Learning comments
- Convolution was a concept I knew about before taking the course. However, it wasn't until this workshop that I understood about the role it plays in image processing as the operation we use to apply a filter to an image.
- The images processed by OpenCV seem to have an overall higher quality, especially with the corner detection filter. This is possibly due to internal optimizations and extra steps that OpenCV takes, such as normalization.
- There were some initial issues with the calculation of the padding for the image. Other than that, the exercise went smoothly.
