clear all 
close all
%% OS DETECTION
% Check what OS I am running on:
if(strcmp(computer(), 'GLNXA64'))
    os = 'linux';
    pathBar = '/';
    sepEnvironment = ':';
elseif(strcmp(computer(), 'PCWIN') || strcmp(computer(), 'PCWIN64'))
    os = 'windows';
    pathBar = '\';
    sepEnvironment = ';';
else
    disp('OS not compatible');
    return;
end
%% CONFIGURE PATHS
% APIRL PATH
apirlPath = '/home/carrolaggi/apirl-code/';
addpath(genpath([apirlPath pathBar 'matlab']));
setenv('PATH', [getenv('PATH') sepEnvironment apirlPath pathBar 'build' pathBar 'bin']);
setenv('LD_LIBRARY_PATH', [getenv('LD_LIBRARY_PATH') sepEnvironment apirlPath pathBar 'build' pathBar 'bin']);

outputPath = '/home/carrolaggi/Desktop/Internship/Simulation3D/';
if ~isdir(outputPath)
    mkdir(outputPath)
end
%% INIT CLASS GPET
PET.scanner = 'mMR';
PET.method =  'otf_siddon_cpu';
PET.PSF.type = 'none';
PET.radialBinTrim = 0;
PET.Geom = '';
PET.sinogram_size.span = 12;
PET.nSubsets = 1;
PET.random_algorithm = 'from_ML_singles_matlab';
PET = classGpet(PET);

%% BRAIN WEB IMAGES
% se cargan y se generan los fantomas

brainWebPath = '/home/carrolaggi/Desktop/Internship/MATLAB_Simu/Phantoms/BrainWEB/BrainWebRaw/';
imgDir = dir ([brainWebPath]);
phantomIndex = 1;
for phantomIndex = 1:1 
% create a PET phantom from brainweb:
disp(phantomIndex);
[pet_rescaled, mumap_rescaled, t1_rescaled, t2_rescaled, classified_tissue_rescaled, maskGrayMatter, maskWhiteMatter, refImage] = createPETPhantomFromBrainweb(strcat(brainWebPath,imgDir(phantomIndex+2).name), [344 344 127], [2.08625 2.08625 2.03125]);
petPhantom = single(pet_rescaled);

 
% Rotate the result 90 degrees around the z-axis


% Symmetry on the x-plane
petPhantom2 = (imrotate(petPhantom, 90, 'bilinear', 'crop'));
petPhantom2 = flipdim(petPhantom2, 3);
% Create 2d phantoms
sliceToProcess = 64;

mumapPhantom = single(mumap_rescaled);
t1Phantom =  single(t1_rescaled);
t2Phantom =  single(t2_rescaled);
classifiedTissuePhantom =  single(classified_tissue_rescaled);
niftiwrite(petPhantom2, [strcat(outputPath,strcat(sprintf('PhantomPet'),string(phantomIndex))) ]);
% info = niftiinfo([outputPath sprintf('PhantomPet')]);
% info.PixelDimensions = PET.image_size.voxelSize_mm;
% niftiwrite(petPhantom, [outputPath sprintf('PhantomPet')], info);
% niftiwrite(mumapPhantom, [outputPath sprintf('PhantomMumap')], info);
% niftiwrite(t1Phantom, [outputPath sprintf('PhantomT1')], info);
% niftiwrite(t2Phantom, [outputPath sprintf('PhantomT2')], info);
% niftiwrite(classifiedTissuePhantom, [outputPath sprintf('PhantomTissues')], info);
end 


%% CREATE GREY MATTER AND WHITE MATTER MASKS
% gmMask = classifiedTissuePhantom == 2;
% wmMask = classifiedTissuePhantom == 3;
% 
% % pixelSize_mm = [2.08625 2.08625 2.03125];
% % xLimits = [-size(petPhantom,2)/2*pixelSize_mm(2) size(petPhantom,2)/2*pixelSize_mm(2)];
% % yLimits = [-size(petPhantom,1)/2*pixelSize_mm(1) size(petPhantom,1)/2*pixelSize_mm(1)];
% % zLimits = [-size(petPhantom,3)/2*pixelSize_mm(3) size(petPhantom,3)/2*pixelSize_mm(3)];
% % refImage = imref3d([size(petPhantom) 1],xLimits,yLimits,zLimits);
% 
% %% SCALE FACTOR TO SET NOISE LEVEL
% counts = 10000000000;
% proj = PET.P(petPhantom); % for any other span
% % Cal factor between counts in image and counts in sinogram:
% calFactor = sum(sum(sum(proj)))/sum(sum(sum(petPhantom)));
% % Rescale the phantom to have the desired
% petGroundTruth = petPhantom./sum(sum(sum(petPhantom)))./calFactor.*counts;
% 
% % % Save the image as a nifti
% % niftiwrite(petGroundTruth, [outputPath sprintf('Pet_Truth')]);
% 
% % Get the meean values for each tissue:
% meanGroundTruthGM = mean(petGroundTruth(gmMask));
% meanGroundTruthWM = mean(petGroundTruth(wmMask));
% stdGroundTruthGM = std(petGroundTruth(gmMask));
% stdGroundTruthWM = std(petGroundTruth(wmMask));
% % Spatial resolution:
% psfFWHM_mm = 5;
% psfStdDev_mm = psfFWHM_mm./2.35;
% psfStdDev_voxels = psfStdDev_mm./PET.image_size.voxelSize_mm(1);
% petGroundTruth_PVE = imgaussfilt(petGroundTruth, 2);
% % Project and introduce noise
% m_sinruido = PET.P(petGroundTruth_PVE); 
% % 
% % Multiplicative correction factors:
% % acf= PET.ACF(mumapPhantom, refImage);
% % % Convert into factors:
% % af = acf;
% % af(af~=0) = 1./ af(af~=0);
% % % Introduce poission noise:
% % y = y.*af;
% m = poissrnd(m_sinruido);
% m_truth = poissrnd(PET.P(petGroundTruth));
% 
% % signal = mean(mean(mean(m_sinruido)))
% % noise = mean(mean(mean(abs(m-m_sinruido))))
% % SNR = 20*log10(signal/noise)
% 
% % % Show images:
% % figure; 
% % subplot(1,3,1);
% % imshow(m_sinruido(:,:,400)', [])
% % subplot(1,3,2);
% % imshow(m(:,:,400)', []);
% % subplot(1,3,3);
% % imshow(m(:,:,400)'-m_sinruido(:,:,400)', [])
% 
% 
% % figure; 
% % subplot(1,4,1);
% % imshow(petGroundTruth(:,:,65), [])
% % subplot(1,4,2);
% % imshow(mumapPhantom(:,:,65), [])
% % subplot(1,4,3);
% % imshow(gmMask(:,:,65), [])
% % subplot(1,4,4);
% % imshow(wmMask(:,:,65), [])
% 
% %% SENSITIVITY IMAGE
% sensImage = PET.PT(ones(size(m)));
% 
% %% RECONSTRUCTION
% k=1;
% numIteraciones = 60;
% Reconstruc_data = struct ('data',PET.ones,'label', PET.ones);
% 
% % figure;
% % set(gcf, "Position", [100 100 1600 1200]);
% % subplot(3,3,1);
% % imshow(sensImage,[]);
% % title('Sensitivity Image');
% % subplot(2,3,2);
% % imshow(m',[]);
% % title('Input Sinogram (m)');
% 
% 
% 
% 
% for k = 1 : numIteraciones
%     disp(k);
%     %MLEM iteration in one line:
%     Reconstruc_data.data = Reconstruc_data.data./(sensImage+1e-5).*PET.PT(m./(PET.P(Reconstruc_data.data)+1e-5));
%     Reconstruc_data.label =Reconstruc_data.label./(sensImage+1e-5).*PET.PT(m_truth./(PET.P(Reconstruc_data.label)+1e-5));
%     % Compute metrics:
%     meanGM(k) = mean(x(gmMask));
%     meanWM(k) = mean(x(wmMask));
%     stdGM(k) = std(x(gmMask));
%     stdWM(k) = std(x(wmMask));
% %     rmse(k) = sqrt(mean(mean((x-petGroundTruth).^2)));
% %     % Plots:
% %     if rem(k,saveInterval_iter) == 0
% %         subplot(2,3,2); imshow(y,[]);
% %         title(sprintf('Estimated Sinogram (y) at iteration %d', k));
% %         subplot(2,3,3); imshow(q,[]);
% %         title(sprintf('Correction Sinogram (q) at iteration %d', k));
% %         subplot(2,3,4); imshow(b,[]);
% %         title(sprintf('Correction Image (b) at iteration %d', k));
% %         subplot(2,3,5); imshow(x,[]);
% %         title(sprintf('Reconstructed Image (x) at iteration %d', k));
% %         pause(0.5);
% %     end
% end
% 
% save(Reconstruc_data);
