package com.robotclient.santosh.robotclient.domain.utils;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.robotclient.santosh.robotclient.domain.pojo.RobotCommand;

import java.lang.reflect.Type;

/**
 * Created by santosh on 06-09-2017.
 */

public class RobotUtility {

    public static String createCommandJson(RobotCommand robotCommand)    {
        Gson gson = new Gson();
        Type type = new TypeToken<RobotCommand>() {}.getType();
        String json = gson.toJson(robotCommand, type);
        android.util.Log.v("JSON", json);
        return json;
    }
}
