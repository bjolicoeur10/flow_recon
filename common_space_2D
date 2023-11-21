clear all
close all

im1 = h5read("Flow1.h5", '/Data/MAG');
im2 = h5read("Flow2.h5", '/Data/MAG');
%im2 = imrotate(im2, 90);
im1 = squeeze(im1(:,:,160));
im2 = squeeze(im2(:,:,160));
figure;
imshow(im1, []);

figure;
imshow(im2, []);

[optimizer, metric] = imregconfig('monomodal');
optimizer.MaximumIterations = 10000;
tform1 = imregtform(im1, im2, 'rigid', optimizer, metric);
registered_image1 = imwarp(im1, tform1, 'OutputView', imref2d(size(im2)));


[optimizer, metric] = imregconfig('monomodal');
optimizer.MaximumIterations = 1000000;
tform2 = imregtform(im2, im1, 'rigid', optimizer, metric);
registered_image2 = imwarp(im2, tform2, 'OutputView', imref2d(size(im1)));

figure;
imshow(registered_image1,[]);
figure;
imshow(registered_image2,[]);

% Extract rotation angles from transformation matrices
angle1 = atan2(tform1.T(2, 1), tform1.T(1, 1));
angle2 = atan2(tform2.T(2, 1), tform2.T(1, 1));

% angle1 = 0.000000001;
% angle2 = 0.000000001;
% Apply half of the calculated rotation to each transformation matrix
store1 = tform1.T;
store2 = tform2.T;
% tform1.T = [cos(angle1/2), -sin(angle1/2), 0; 
%             sin(angle1/2), cos(angle1/2), 0; 
%             -66, 160, 1];
% 
% tform2.T = [cos(angle2/2), -sin(angle2/2), 0; 
%             sin(angle2/2), cos(angle2/2), 0; 
%             160, -66, 1];
size1 = 226.27;
v31 = size1 -  size1* cos(angle1/2);
v32 = -size1 * sin(angle1/2);
v33 = size1 - size1 * cos(angle2/2);
v34 = -size1 * sin(angle2/2);
tform1.T = [cos(angle1/2), -sin(angle1/2), 0; 
            sin(angle1/2), cos(angle1/2), 0; 
            -v31, -v32, 1];

tform2.T = [cos(angle2/2), -sin(angle2/2), 0; 
            sin(angle2/2), cos(angle2/2), 0; 
            v34, -v33, 1];








% Apply the updated transformations to the images
registered_image1 = imwarp(im1, tform1, 'OutputView', imref2d([320 320]));
registered_image2 = imwarp(im2, tform2, 'OutputView', imref2d([320 320]));

% Display the aligned images
figure;
imshow(registered_image1, []);
title('Registered Image 1');

figure;
imshow(registered_image2, []);
title('Registered Image 2');


matrix1 = im1;
matrix2 = im2;

vector1 = matrix1(:);
vector2 = matrix2(:);

differences = vector1 - vector2;
averages = (vector1 + vector2) / 2;


mean_diff = mean(differences);
std_diff = std(differences);
upper_limit = mean_diff + 1.96 * std_diff; % 95% limits of agreement
lower_limit = mean_diff - 1.96 * std_diff;

plot(averages, differences, 'o');
hold on;
line([min(averages) max(averages)], [mean_diff mean_diff], 'Color', 'red'); % Mean line
line([min(averages) max(averages)], [upper_limit upper_limit], 'Color', 'black', 'LineStyle', '--'); % Upper limit
line([min(averages) max(averages)], [lower_limit lower_limit], 'Color', 'black', 'LineStyle', '--'); % Lower limit

xlabel('Average of Measurements');
ylabel('Difference between Measurements');
title('Bland-Altman Plot');

legend('Differences', 'Mean Difference', '95% Limits of Agreement', 'Location', 'best');

fprintf('Mean Difference: %.4f\n', mean_diff);
fprintf('95%% Limits of Agreement: [%.4f, %.4f]\n', lower_limit, upper_limit);
