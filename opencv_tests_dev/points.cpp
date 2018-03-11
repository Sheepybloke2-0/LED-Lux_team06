#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/calib3d/calib3d.hpp>
#include <opencv2/features2d/features2d.hpp>

using namespace std;

int main() {
  //string gst = "v4l2src device=/dev/video0 ! video/x-raw, width=640, height=480, format=BGR ! videoconvert ! appsink";
  cv::VideoCapture input(0);//input(gst, cv::CAP_GSTREAMER);

  cv::Mat img;
  // https://docs.opencv.org/2.3/modules/features2d/doc/common_interfaces_of_feature_detectors.html
  // Don't need too many features
  Ptr<ORB> detector = cv::ORB::create(50);
  std::vector<cv::KeyPoint> img_kp;

  for (;;)
  {
    // Read an image from the input camera
    if (!input.read(img))
    {
      break;
    }

    detector(img, cv::Mat(), img_kp);
    drawKeypoints(img, img_kp, img);

    cv:imshow("img", img);

    // Wait for ESC key
    if (cv::waitKey() == 27 )
    {
      break;
    }
  }


  return 0;
}
