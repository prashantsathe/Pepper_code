package com.robotclient.santosh.robotclient.presenter;

import android.app.Activity;
import android.content.Context;
import android.support.annotation.NonNull;

/**
 * Created by santosh on 22-09-2017.
 */

public interface PermissionsPresenter {

    public void requestPermission(Activity context);
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults);

    interface Callback {
        public void onPermissionsGranted();
        public void onPermissionsDenied();
    }
}
