package com.robotclient.santosh.robotclient.view.activity;

import android.graphics.Bitmap;
import android.graphics.SurfaceTexture;
import android.media.MediaMetadataRetriever;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.MotionEvent;
import android.view.Surface;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.TextureView;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.VideoView;

import com.robotclient.santosh.robotclient.R;
import com.robotclient.santosh.robotclient.presenter.RobotConnectionPresenter;
import com.robotclient.santosh.robotclient.presenter.RobotConnectionPresenterImpl;
import com.robotclient.santosh.robotclient.presenter.RobotNavigation;
import com.robotclient.santosh.robotclient.presenter.RobotNavigationPresenterImpl;
import com.robotclient.santosh.robotclient.presenter.TextureViewPresenter;
import com.robotclient.santosh.robotclient.presenter.TextureViewPresenterImpl;
import com.robotclient.santosh.robotclient.view.CircularSeekBar;

import java.io.IOException;

public class PepperMainActivity extends AppCompatActivity implements SurfaceHolder.Callback, MediaPlayer.OnPreparedListener,
        View.OnTouchListener {
    private static final String TAG = PepperMainActivity.class.getName();
    private SurfaceHolder surfaceHolder;
    private MediaPlayer mediaPlayer;
    final static String RTSP_URL = "http://videocdn.bodybuilding.com/video/mp4/62000/62792m.mp4"; //"tcp://10.9.45.84:9559" ;
    private TextureViewPresenter textureViewPresenter;
    private RobotConnectionPresenter robotConnectionPresenter = new RobotConnectionPresenterImpl();
    private RobotNavigation robotNavigation= new RobotNavigationPresenterImpl();
    private static Boolean initBar = false;
    private TextView mTvTop;
    private CircularSeekBar circularSeekBar;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        Window window = getWindow();
        Log.d(TAG,"onCreate()");
        window.setFlags(
                WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);
        window.setBackgroundDrawableResource(android.R.color.black);
        setContentView(R.layout.activity_pepper_main);
        mTvTop = (TextView)findViewById(R.id.top_tv) ;
        mTvTop.setOnTouchListener(this);
        //setupVideoView();
        //setupVideoView1();
        //setupMediaRetriever();
        //setupTextureView();
        init();
    }

    private void init() {
        circularSeekBar = (CircularSeekBar) findViewById(R.id.angle_sb);
        circularSeekBar.setOnSeekBarChangeListener(seekBarChangeListener);
        circularSeekBar.setProgress(50);
    }


    private void setupVideoView()   {
        SurfaceView surfaceView =
                (SurfaceView) findViewById(R.id.surfaceView);
        surfaceHolder = surfaceView.getHolder();
        surfaceHolder.addCallback(this);
        surfaceHolder.setFixedSize(320, 240);
    }

    @Override
    public void surfaceCreated(final SurfaceHolder surfaceHolder) {

       /* Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                mediaPlayer = new MediaPlayer();
                mediaPlayer.setDisplay(surfaceHolder);
                Uri uri = Uri.parse(RTSP_URL);
                try {
                    mediaPlayer.setDataSource(getApplicationContext(),uri);
                    mediaPlayer.setOnPreparedListener(PepperMainActivity.this);
                    mediaPlayer.prepareAsync();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
        thread.start();

        mediaPlayer = new MediaPlayer();
        mediaPlayer.setDisplay(surfaceHolder);
        Uri uri = Uri.parse(RTSP_URL);
        try {
            mediaPlayer.setDataSource(getApplicationContext(),uri);
            mediaPlayer.setOnPreparedListener(PepperMainActivity.this);
            mediaPlayer.prepareAsync();
        } catch (IOException e) {
            e.printStackTrace();
        } */

    }

    @Override
    public void surfaceChanged(SurfaceHolder surfaceHolder, int i, int i1, int i2) {

    }

    @Override
    public void surfaceDestroyed(SurfaceHolder surfaceHolder) {

    }

    @Override
    public void onPrepared(MediaPlayer mediaPlayer) {
        mediaPlayer.start();
    }


    private void setupVideoView1()   {
        VideoView myVideoView = (VideoView)findViewById(R.id.videoView);
        myVideoView.setVideoURI(Uri.parse(RTSP_URL));
        android.widget.MediaController mediaController = new android.widget.MediaController(this);
        mediaController.setAnchorView(myVideoView);
        myVideoView.setMediaController(mediaController);
        myVideoView.requestFocus();
        myVideoView.start();
    }


    private void setupMediaRetriever()  {
        final MediaMetadataRetriever mediaMetadataRetriever = new MediaMetadataRetriever();
        mediaMetadataRetriever.setDataSource(RTSP_URL);
        final VideoView myVideoView = (VideoView)findViewById(R.id.videoView);
        myVideoView.setVideoURI(Uri.parse(RTSP_URL));
        android.widget.MediaController mediaController = new android.widget.MediaController(this);
        mediaController.setAnchorView(myVideoView);
        myVideoView.setMediaController(mediaController);
        myVideoView.requestFocus();
        myVideoView.start();
        Button buttonCapture = (Button)findViewById(R.id.button);

        buttonCapture.setOnClickListener(new View.OnClickListener(){

            @Override
            public void onClick(View arg0) {

                int currentPosition = myVideoView.getCurrentPosition(); //in millisecond
                Toast.makeText(getApplicationContext(),
                        "Current Position: " + currentPosition + " (ms)",
                        Toast.LENGTH_LONG).show();

                Bitmap bmFrame = mediaMetadataRetriever
                        .getFrameAtTime(currentPosition * 1000); //unit in microsecond

                if(bmFrame == null){
                    Toast.makeText(getApplicationContext(),
                            "bmFrame == null!",
                            Toast.LENGTH_LONG).show();
                }else{
                    AlertDialog.Builder myCaptureDialog =
                            new AlertDialog.Builder(getApplicationContext());
                    ImageView capturedImageView = new ImageView(getApplicationContext());
                    capturedImageView.setImageBitmap(bmFrame);
                    ViewGroup.LayoutParams capturedImageViewLayoutParams =
                            new ViewGroup.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT,
                                    ViewGroup.LayoutParams.WRAP_CONTENT);
                    capturedImageView.setLayoutParams(capturedImageViewLayoutParams);

                    myCaptureDialog.setView(capturedImageView);
                    myCaptureDialog.show();
                }

            }});
    }
    private  TextureView textureView;
    private void setupTextureView() {
        textureView = (TextureView) findViewById(R.id.textureView);
        textureViewPresenter = new TextureViewPresenterImpl(textureView);

        final MediaPlayer.OnBufferingUpdateListener onBufferingUpdateListener = new MediaPlayer.OnBufferingUpdateListener() {

            @Override
            public void onBufferingUpdate(MediaPlayer mediaPlayer, int i) {

            }
        };

        final MediaPlayer.OnCompletionListener onCompletionListener = new MediaPlayer.OnCompletionListener() {

            @Override
            public void onCompletion(MediaPlayer mediaPlayer) {

            }
        };

        final MediaPlayer.OnPreparedListener onPreparedListener = new MediaPlayer.OnPreparedListener() {

            @Override
            public void onPrepared(MediaPlayer mediaPlayer) {

            }
        };

        final MediaPlayer.OnVideoSizeChangedListener onVideoSizeChangedListener = new MediaPlayer.OnVideoSizeChangedListener() {

            @Override
            public void onVideoSizeChanged(MediaPlayer mediaPlayer, int i, int i1) {

            }
        };

        final MediaPlayer.OnErrorListener onErrorListener = new MediaPlayer.OnErrorListener() {
            @Override
            public boolean onError(MediaPlayer mediaPlayer, int i, int i1) {
                mediaPlayer.reset();
                return false;
            }
        };

        final TextureView.SurfaceTextureListener surfaceTextureListener = new TextureView.SurfaceTextureListener() {

            @Override
            public void onSurfaceTextureAvailable(SurfaceTexture surfaceTexture, int i, int i1) {
                Surface s = new Surface(surfaceTexture);

                try {
                    MediaPlayer mp = new MediaPlayer();
                    mp.setDataSource(RTSP_URL);
                    mp.setSurface(s);
                    mp.prepare();
                   // mp.setLooping(true);
                    mp.setOnBufferingUpdateListener(onBufferingUpdateListener);
                    mp.setOnCompletionListener(onCompletionListener);
                    mp.setOnPreparedListener(onPreparedListener);
                    mp.setOnVideoSizeChangedListener(onVideoSizeChangedListener);

                    //mp.setAudioStreamType(AudioManager.STREAM_MUSIC);
                    mp.start();

                    Button b = (Button) findViewById(R.id.button);
                    b.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View v) {
                            // threadExecutor.execute();
                            textureViewPresenter.saveFrame();
                        }
                    });
                } catch (IllegalArgumentException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                } catch (SecurityException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                } catch (IllegalStateException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }

            @Override
            public void onSurfaceTextureSizeChanged(SurfaceTexture surfaceTexture, int i, int i1) {

            }

            @Override
            public boolean onSurfaceTextureDestroyed(SurfaceTexture surfaceTexture) {
                return false;
            }

            @Override
            public void onSurfaceTextureUpdated(SurfaceTexture surfaceTexture) {

            }
        };

       textureView.setSurfaceTextureListener(surfaceTextureListener);
    }

    public void onClick(View view) {
        Log.v(TAG,"OnClick command pre process started ..");
        String command;
        try {
            switch (view.getId()) {
                case R.id.left_tv:
                    //textureViewPresenter.saveFrame();
                    //mCamera.takePicture(null, null, mPicture);
                    //command = robotNavigation.moveToLeft();
                    //robotConnectionPresenter.writeToConnection(command);
                    break;
                case R.id.right_tv:
                    //mCamera.takePicture(null, null, mPicture);
                    //textureViewPresenter.saveFrame();
                    //command=robotNavigation.moveToRight();
                    //robotConnectionPresenter.writeToConnection(command);
                    break;
                case R.id.top_tv:
                    //textureViewPresenter.saveFrame();
                    //mCamera.takePicture(null, null, mPicture);
                    command = robotNavigation.stop();
                    robotConnectionPresenter.writeToConnection(command);
                    break;
                case R.id.bottom_tv:
                    //textureViewPresenter.saveFrame();
                    // mCamera.takePicture(null, null, mPicture);
                    //command = robotNavigation.moveBackward();
                    //robotConnectionPresenter.writeToConnection(command);
                    break;
                case R.id.stop_tv:
                    textureViewPresenter.saveFrame();
                    // mCamera.takePicture(null, null, mPicture);
                    //command = robotNavigation.stop();
                    //robotConnectionPresenter.writeToConnection(command);
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
    private CircularSeekBar.OnCircularSeekBarChangeListener seekBarChangeListener = new
            CircularSeekBar.OnCircularSeekBarChangeListener() {
                String command;
                @Override
                public void onProgressChanged(CircularSeekBar circularSeekBar, int progress, boolean fromUser) {

                    if (initBar == false) {
                        initBar = true;
                        return;
                    }
                    if(progress>=50){
                        robotNavigation.updateNavigationTheta(progress);
                        command=robotNavigation.moveToRightTheta();
                        robotConnectionPresenter.writeToConnection(command);
                    }else{
                        robotNavigation.updateNavigationTheta(progress);
                        command=robotNavigation.moveToLeftTheta();
                        robotConnectionPresenter.writeToConnection(command);
                    }
                }

                @Override
                public void onStopTrackingTouch(CircularSeekBar seekBar) {
                    command = robotNavigation.stop();
                    robotConnectionPresenter.writeToConnection(command);
                    circularSeekBar.setProgress(50);
                }

                @Override
                public void onStartTrackingTouch(CircularSeekBar seekBar) {

                }
            };


    @Override
    public boolean onTouch(View view, MotionEvent event) {
        boolean isReleased = event.getAction() == MotionEvent.ACTION_UP || event.getAction() == MotionEvent.ACTION_CANCEL;
        boolean isPressed = event.getAction() == MotionEvent.ACTION_DOWN;

        if (isPressed) {
            String command =robotNavigation.moveStright();
            robotConnectionPresenter.writeToConnection(command);
        }
        return false;
    }
}
