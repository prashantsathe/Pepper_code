package com.robotclient.santosh.robotclient.domain.pojo;

/**
 * Created by santosh on 06-09-2017.
 */

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class RobotCommand {

    @SerializedName("command")
    @Expose
    private Command command;

    public Command getCommand() {
        return command;
    }

    public void setCommand(Command command) {
        this.command = command;
    }


    public static class Command {

        @SerializedName("api")
        @Expose
        private String api;
        @SerializedName("parameters")
        @Expose
        private Parameters parameters;

        public String getApi() {
            return api;
        }

        public void setApi(String api) {
            this.api = api;
        }

        public Parameters getParameters() {
            return parameters;
        }

        public void setParameters(Parameters parameters) {
            this.parameters = parameters;
        }

    }

    public static class Parameters {

        @SerializedName("x")
        @Expose
        private Double x;
        @SerializedName("y")
        @Expose
        private Double y;
        @SerializedName("theta")
        @Expose
        private Double theta;

        public Double getX() {
            return x;
        }

        public void setX(Double x) {
            this.x = x;
        }

        public Double getY() {
            return y;
        }

        public void setY(Double y) {
            this.y = y;
        }

        public Double getTheta() {
            return theta;
        }

        public void setTheta(Double theta) {
            this.theta = theta;
        }
    }

}



