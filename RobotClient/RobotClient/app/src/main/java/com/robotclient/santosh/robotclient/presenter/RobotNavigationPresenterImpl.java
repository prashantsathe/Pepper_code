package com.robotclient.santosh.robotclient.presenter;

import com.robotclient.santosh.robotclient.domain.pojo.RobotCommand;
import com.robotclient.santosh.robotclient.domain.utils.RobotUtility;

/**
 * Created by santosh on 06-09-2017.
 */

public class RobotNavigationPresenterImpl implements RobotNavigation{
    private double MAX_PROGRESS=100;
    private double leftToRightTheta;
    private double rightToLeftTheta;
    @Override
    public String moveToLeft() {
        String command = generateRobotCommand(0.5,0.0,rightToLeftTheta,"moveToward");
        return command;
    }

    @Override
    public String moveToRight() {
        String command =generateRobotCommand(0.5,0.0,leftToRightTheta,"moveToward");
        return command;
    }

    @Override
    public String moveForward() {
        String command =generateRobotCommand(1,0.0,0.0,"moveToward");
        return command;
    }

    @Override
    public String moveBackward() {
        String command =generateRobotCommand(-0.5,0.0,0.0,"moveToward");
        return command;
    }

    @Override
    public String moveToLeftTheta() {
        String command =generateRobotCommand(0.0,0.0,rightToLeftTheta,"moveToward");
        return command;
    }

    @Override
    public String moveToRightTheta() {
        String command =generateRobotCommand(0.0,0.0,leftToRightTheta,"moveToward");
        return command;
    }

    @Override
    public String moveStright() {
        String command =generateRobotCommand(0.5,0.0,0,"moveToward");
        return command;
    }


    @Override
    public String stop() {
        String command =generateRobotCommand(0.0,0.0,0.0,"stopMove");
        return command;
    }

    @Override
    public void updateNavigationTheta(int progress) {
        leftToRightTheta = progress/MAX_PROGRESS; // Clock wise rotation.
        rightToLeftTheta = (progress-MAX_PROGRESS)/MAX_PROGRESS; //Anti clock wise rotation
    }

    private String generateRobotCommand(double x, double y, double theta,String apiType) {
        RobotCommand robotCommand = new RobotCommand();
        RobotCommand.Command command = new RobotCommand.Command();
        RobotCommand.Parameters parameters = new RobotCommand.Parameters();
        parameters.setTheta(theta);
        parameters.setX(x);
        parameters.setY(y);
        command.setApi(apiType);
        command.setParameters(parameters);
        robotCommand.setCommand(command);
        String jsonString = RobotUtility.createCommandJson(robotCommand) + "\n";
        return jsonString;
    }

}
