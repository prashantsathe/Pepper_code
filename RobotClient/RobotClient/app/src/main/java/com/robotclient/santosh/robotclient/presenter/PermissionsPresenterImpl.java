package com.robotclient.santosh.robotclient.presenter;

import android.Manifest;
import android.app.Activity;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;

/**
 * Created by santosh on 22-09-2017.
 */

public class PermissionsPresenterImpl implements PermissionsPresenter{

    private static final String[] PERMISSIONS = {
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.CAMERA};
    private static final int PERMISSION_ALL = 0x0001;
    private int[] checkedPermissions = new int[PERMISSIONS.length];
    private PermissionsPresenter.Callback callback;

    public PermissionsPresenterImpl(PermissionsPresenter.Callback callback)  {
        this.callback = callback;
    }

    @Override
    public void requestPermission(Activity activity) {
        boolean isPermissionRequested=false;
        for(int i=0; i<PERMISSIONS.length;i++) {
            checkedPermissions[i] = ActivityCompat.checkSelfPermission(activity, PERMISSIONS[i]);
        }
        ActivityCompat.requestPermissions(activity, PERMISSIONS, PERMISSION_ALL);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        switch(requestCode) {
            case PERMISSION_ALL :
                for(String permission : permissions) {

                    if( !Manifest.permission.WRITE_EXTERNAL_STORAGE.equals(permission)) {
                        return;
                    }

                    if( !Manifest.permission.CAMERA.equals(permission)) {
                        return;
                    }
                }
                callback.onPermissionsGranted();
        }
    }
}
