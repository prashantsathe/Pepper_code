package com.robotclient.santosh.robotclient.presenter;

import android.graphics.Bitmap;
import android.os.Environment;
import android.util.Log;
import android.view.TextureView;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

/**
 * Created by santosh on 12-09-2017.
 */

public class TextureViewPresenterImpl implements TextureViewPresenter {
    private static final String TAG = TextureViewPresenterImpl.class.getName();
    private ThreadExecutor executor;
    private TextureView textureView;

    public TextureViewPresenterImpl(TextureView textureView) {
        this.textureView = textureView;
        executor=new ThreadExecutor();
    }

    @Override
    public void saveFrame() {
        executor.execute();
    }



    public class ThreadExecutor {
        private final int CORE_POOL_SIZE = Runtime.getRuntime().availableProcessors();
        private final int MAX_POOL_SIZE = CORE_POOL_SIZE;
        private final int KEEP_ALIVE_TIME = 120;
        private final TimeUnit TIME_UNIT = TimeUnit.SECONDS;
        private final BlockingQueue<Runnable> WORK_QUEUE = new LinkedBlockingQueue<Runnable>();
        private ThreadPoolExecutor mThreadPoolExecutor;

        ThreadExecutor() {
            long keepAlive = KEEP_ALIVE_TIME;

            mThreadPoolExecutor = new ThreadPoolExecutor(
                    CORE_POOL_SIZE,
                    MAX_POOL_SIZE,
                    keepAlive,
                    TIME_UNIT,
                    WORK_QUEUE);

        }

        public void execute() {
            mThreadPoolExecutor.submit(new Runnable() {
                @Override
                public void run() {
                    String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmssSS").format(new Date());
                    File sdcard = Environment.getExternalStorageDirectory();
                    File texture = new File(sdcard,"TexturePictures");
                    if(!texture.exists()) {
                        texture.mkdir();
                    }
                    File captureImage = new File(texture,timeStamp + ".png");
                   /* String mPath = Environment.getExternalStorageDirectory().toString()
                            + "/Pictures/" + timeStamp + ".png";*/
                    //      Toast.makeText(getApplicationContext(), "Capturing Screenshot: " + mPath, Toast.LENGTH_SHORT).show();
                    Bitmap bm;
                    synchronized (textureView) {
                        bm = textureView.getBitmap();
                    }
                    if(bm == null)
                        Log.e(TAG,"bitmap is null");

                    OutputStream fout = null;
                    File imageFile = new File(captureImage.toString());

                    try {
                        fout = new FileOutputStream(imageFile);
                        bm.compress(Bitmap.CompressFormat.PNG, 90, fout);
                        fout.flush();
                        fout.close();
                        bm=null;
                    } catch (FileNotFoundException e) {
                        Log.e(TAG, "FileNotFoundException");
                        e.printStackTrace();
                    } catch (IOException e) {
                        Log.e(TAG, "IOException");
                        e.printStackTrace();
                    }
                }
            });
        }
    }
}
