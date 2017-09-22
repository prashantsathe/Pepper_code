package com.robotclient.santosh.robotclient;

import android.content.Context;
import android.content.pm.PackageManager;
import android.hardware.Camera;
import android.os.Bundle;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.FrameLayout;

import com.robotclient.santosh.robotclient.presenter.RobotConnectionPresenter;
import com.robotclient.santosh.robotclient.presenter.RobotConnectionPresenterImpl;
import com.robotclient.santosh.robotclient.presenter.RobotNavigation;
import com.robotclient.santosh.robotclient.presenter.RobotNavigationPresenterImpl;
import com.robotclient.santosh.robotclient.presenter.TextureViewPresenter;
import com.robotclient.santosh.robotclient.presenter.TextureViewPresenterImpl;
import com.robotclient.santosh.robotclient.view.CircularSeekBar;
import com.robotclient.santosh.robotclient.view.customView.CameraTexturePreview;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "ROBOT_CAMERA";
    public static final int MEDIA_TYPE_IMAGE = 1;
    public static final int MEDIA_TYPE_VIDEO = 2;
    private Camera mCamera;
    private CameraPreview mPreview;
    private CameraTexturePreview cameraTexturePreview;
    private RobotConnectionPresenter robotConnectionPresenter = new RobotConnectionPresenterImpl();
    private RobotNavigation robotNavigation= new RobotNavigationPresenterImpl();
    private TextureViewPresenter textureViewPresenter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
       // setupCamera();
        init();
    }

    private void init() {
        CircularSeekBar circularSeekBar = (CircularSeekBar) findViewById(R.id.angle_sb);
        circularSeekBar.setOnSeekBarChangeListener(seekBarChangeListener);
        circularSeekBar.setProgress(50);
    }

    /**
     * Create our Preview view
     * and set it as the content of our activity
     */
    private void setupCamera()  {
        mCamera = getCameraInstance();
        //mPreview = new CameraPreview(this, mCamera);
        cameraTexturePreview= new CameraTexturePreview(this,mCamera);
        FrameLayout preview = (FrameLayout) findViewById(R.id.camera_preview);
        //preview.addView(mPreview,0);
        preview.addView(cameraTexturePreview,0);
        textureViewPresenter=new TextureViewPresenterImpl(cameraTexturePreview);
    }

    /** Check if this device has a camera */
    private boolean checkCameraHardware(Context context) {
        if (context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_CAMERA)){
            return true;
        } else {
            return false;
        }
    }

    /**
     * A safe way to get an instance of the Camera object.
     */
    public static Camera getCameraInstance(){
        Camera c = null;
        try {
            c = Camera.open();
        }
        catch (Exception e){
            e.printStackTrace();
        }
        return c;
    }

    private void releaseCamera(){
        if (mCamera != null){
            mCamera.release();        // release the camera for other applications
            mCamera = null;
        }
    }

    public void onClick(View view) {
        Log.v(TAG,"OnClick command pre process started ..");
        String command;
        try {
            switch (view.getId()) {
                case R.id.left_tv:
                    textureViewPresenter.saveFrame();
                    //mCamera.takePicture(null, null, mPicture);
                    command = robotNavigation.moveToLeft();
                    robotConnectionPresenter.writeToConnection(command);
                    break;
                case R.id.right_tv:
                    //mCamera.takePicture(null, null, mPicture);
                    textureViewPresenter.saveFrame();
                    command=robotNavigation.moveToRight();
                    robotConnectionPresenter.writeToConnection(command);
                    break;
                case R.id.top_tv:
                    textureViewPresenter.saveFrame();
                    //mCamera.takePicture(null, null, mPicture);
                    command=robotNavigation.moveForward();
                    robotConnectionPresenter.writeToConnection(command);
                    break;
                case R.id.bottom_tv:
                    textureViewPresenter.saveFrame();
                   // mCamera.takePicture(null, null, mPicture);
                    command = robotNavigation.moveBackward();
                    robotConnectionPresenter.writeToConnection(command);
                    break;
                case R.id.stop_tv:
                    textureViewPresenter.saveFrame();
                    // mCamera.takePicture(null, null, mPicture);
                    command = robotNavigation.stop();
                    robotConnectionPresenter.writeToConnection(command);
                    break;
                default:
            }
        }catch(Exception e) {
            e.printStackTrace();
        }
    }

    private String createCommand(float x, float y, float theta){
        StringBuilder sb = new StringBuilder();
        String command = sb.append(x).append(":").append(y).append(":").append(theta).toString();
        return command;
    }

    private Camera.PictureCallback mPicture = new Camera.PictureCallback() {

        @Override
        public void onPictureTaken(byte[] data, Camera camera) {
            File pictureFile = getOutputMediaFile(MEDIA_TYPE_IMAGE);
            if (pictureFile == null) {
                Log.d(TAG, "Error creating media file, check storage permissions:");
                return;
            }

            try {
                FileOutputStream fos = new FileOutputStream(pictureFile);
                fos.write(data);
                fos.close();
                mCamera.startPreview();
            } catch (FileNotFoundException e) {
                Log.d(TAG, "File not found: " + e.getMessage());
            } catch (IOException e) {
                Log.d(TAG, "Error accessing file: " + e.getMessage());
            }
        }
    };

    /** Create a File for saving an image or video */
    private static File getOutputMediaFile(int type){
        // To be safe, you should check that the SDCard is mounted
        // using Environment.getExternalStorageState() before doing this.
        File mediaStorageDir = new File(Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_PICTURES), "RobotPictures");
        // This location works best if you want the created images to be shared
        // between applications and persist after your app has been uninstalled.
        // Create the storage directory if it does not exist
        if (! mediaStorageDir.exists()){
            if (! mediaStorageDir.mkdirs()){
                Log.d("MyCameraApp", "failed to create directory");
                return null;
            }
        }
        // Create a media file name
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        File mediaFile;
        if (type == MEDIA_TYPE_IMAGE){
            mediaFile = new File(mediaStorageDir.getPath() + File.separator +
                    "IMG_"+ timeStamp + ".jpg");
        } else if(type == MEDIA_TYPE_VIDEO) {
            mediaFile = new File(mediaStorageDir.getPath() + File.separator +
                    "VID_"+ timeStamp + ".mp4");
        } else {
            return null;
        }
        return mediaFile;
    }


    private CircularSeekBar.OnCircularSeekBarChangeListener seekBarChangeListener = new
            CircularSeekBar.OnCircularSeekBarChangeListener() {
                @Override
                public void onProgressChanged(CircularSeekBar circularSeekBar, int progress, boolean fromUser) {
                    /*robotNavigation.updateNavigationTheta(progress);
                    robotConnectionPresenter.writeToConnection(createCommand(0, 0, progress));*/

                    Log.d("Robot","Moving to"+progress);
                }

                @Override
                public void onStopTrackingTouch(CircularSeekBar seekBar) {

                }

                @Override
                public void onStartTrackingTouch(CircularSeekBar seekBar) {

                }
            };
}
