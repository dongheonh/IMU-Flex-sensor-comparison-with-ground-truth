clear, clc 
close all
load data

cut1 = 500;
angles = angles(1,1:cut1);
imu = imu(1,1:cut1);
voltage = voltage(1,1:cut1);

t = 1:cut1;
figure(1)
plot(t,angles, LineWidth=1.5)
hold on
plot(t,imu, LineWidth=1.5)

legend('ground truth angles','imu agnles')

%% Calibration part: Quadratic interpolation (fitting a second-degree polynomial)
p = polyfit(voltage, angles, 2);  % Fit polynomial of degree 2

% Generating a range of voltage values for plotting the fitted curve
voltage_range = linspace(min(voltage), max(voltage), cut1);
angles_fitted = polyval(p, voltage_range);  % Evaluate polynomial

% Plotting
figure;
plot(voltage, angles, '*', 'DisplayName', 'Original Data');
hold on;
plot(voltage_range, angles_fitted, 'r-', 'LineWidth', 1.5, 'DisplayName', 'Quadratic Fit');
xlabel('Voltage');
ylabel('Angle (degrees)');
legend('show');
title('Quadratic Fit of Voltage vs. Angles');

% Calculating RMSE between original angles and fitted angles using the original voltage data
angles_estimated = polyval(p, voltage);  % Estimate angles from original voltage data
rmse = sqrt(mean((angles - angles_estimated).^2));

disp(['RMSE between original angles and angles estimated from quadratic fit: ', num2str(rmse)]);

%% show the angle
angle_calibrated = clb(voltage,p);
figure(3)
plot(t,angle_calibrated)
figure(4)
plot(t,angle_calibrated,LineWidth=1.5)
hold on
plot(t,imu,LineWidth=1.5)
legend('flex angle','imu agnles')

figure(5)
plot(t,angle_calibrated,LineWidth=1.5)
hold on
plot(t,imu,LineWidth=1.5)
plot(t,angles, LineWidth=1.5)
legend('flex angle','imu agnles', 'ground truth')

figure(6)
plot(t,angle_calibrated,LineWidth=1.5)
hold on
plot(t,angles, LineWidth=1.5)
legend('flex angle', 'ground truth')

%% short amount of time hysteris
cut = 100;
angles2 = angles(1,1:cut);
voltage2 = voltage(1,1:cut);
angle_calibrated2 = clb(voltage2,p);
t2 = 1:cut;

figure(7)

plot(t2,angle_calibrated2,LineWidth=1.5)
hold on
plot(t2,angles2, LineWidth=1.5)




function angle = clb(voltage, p)
    % Corrected variable names and equation format
    angle = p(1).*voltage.^2 + p(2).*voltage + p(3);
end






