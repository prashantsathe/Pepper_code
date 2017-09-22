package com.robotclient.santosh.robotclient.view.customView;

import android.content.Context;
import android.graphics.SurfaceTexture;
import android.hardware.Camera;
import android.util.Log;
import android.view.TextureView;

import java.io.IOException;

import static android.content.ContentValues.TAG;

/**
 * Created by santosh on 12-09-2017.
 */

public class CameraTexturePreview extends TextureView implements TextureView.SurfaceTextureListener{
    private Camera mCamera;

    public CameraTexturePreview(Context context, Camera camera) {
        super(context);
        mCamera=camera;
        setSurfaceTextureListener(this);
    }

    @Override
    public void onSurfaceTextureAvailable(SurfaceTexture surfaceTexture, int i, int i1) {
        try {
            if(mCamera==null) return;
            mCamera.setPreviewTexture(surfaceTexture);
            mCamera.startPreview();
        } catch (IOException e) {
            Log.d(TAG, "Error setting camera preview: " + e.getMessage());
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
}
