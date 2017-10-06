package com.robotclient.santosh.robotclient.presenter;

/**
 * Created by santosh on 06-09-2017.
 */

public interface RobotNavigation {
    public String moveToLeft();
    public String moveToRight();
    public String moveForward();
    public String moveBackward();
    public String moveToLeftTheta();
    public String moveToRightTheta();
    public String moveStraight();
    public String stop();
    public void updateNavigationTheta(int progress);
    public String navigate();
    public String localize();
}
