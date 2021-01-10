clear;close all;
% 初始化v-rep接口组件
vrep = remApi('remoteApi');     % using the prototype file (remoteApiProto.m)
vrep.simxFinish(-1);            % just in case, close all opened connections
clientID = vrep.simxStart('127.0.0.1',19997,true,true,5000,5);
if clientID < 0
    disp('Failed connecting to remote API server');    
else
    vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot);
    % 获取速度和图片的句柄
    [res, motorLeft] = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_blocking);
    [res, motorRight] = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_blocking);
    [res, camera] = vrep.simxGetObjectHandle(clientID,'Vision_sensor',vrep.simx_opmode_blocking);
    err = 0;
    while 1
        % 获取当前图像
        code = 1;
        while code
            [code, size, img] = vrep.simxGetVisionSensorImage2(clientID, camera, 1, vrep.simx_opmode_oneshot);
        end
        if min(min(img(:,:))) > 20
            vrep.simxSetJointTargetVelocity(clientID, motorLeft, direct, vrep.simx_opmode_oneshot);
            vrep.simxSetJointTargetVelocity(clientID, motorRight, -direct, vrep.simx_opmode_oneshot);
            while img(480,320) > 20
                code = 1;
                while code
                    [code, size, img] = vrep.simxGetVisionSensorImage2(clientID, camera, 1, vrep.simx_opmode_oneshot);
                end
            end
            err = 0;
            new_err = 0;
        else
            [new_err, direct_tmp] = getErr(img);
            if direct_tmp ~= 0
                direct = direct_tmp;
            end
            v = 2;
            kp = 0.02;
            kd = 0.001;
            delta_v = kp * new_err + kd * (new_err - err);
            err = new_err;
            vrep.simxSetJointTargetVelocity(clientID, motorLeft, v + delta_v, vrep.simx_opmode_oneshot);
            vrep.simxSetJointTargetVelocity(clientID, motorRight, v - delta_v, vrep.simx_opmode_oneshot);
        end
    end
    vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait);
    vrep.simxFinish(clientID);
    vrep.delete(); % call the destructor
end

function [err, direct] = getErr(img)
    err = 1000000;
    err2 = 1000000;
    flag = 0;
    direct = 0;
    distance = 480;
    while err == 1000000
        for i = 1:640
            if img(distance, i) < 20 && flag == 0
                l = i;
                flag = 1;
            end
            if img(distance, i) >20 && flag == 1
                r = i;
                flag = 0;
                dis = (r + l) / 2 - 320;
                if abs(dis) < abs(err)
                    if err == 1000000
                        direct = 0;
                    elseif err < 0
                        err2 = err;
                        direct = -1;
                    else
                        err2 = err;
                        direct = 1;
                    end
                    err = dis;
                elseif abs(dis) < abs(err2)
                    err2 = dis;
                    if err2 < 0
                        direct = -1;
                    else
                        direct = 1;
                    end                   
                end
            end
        end
        distance = distance - 1;
        if distance <= 360
            break
        end
    end
end