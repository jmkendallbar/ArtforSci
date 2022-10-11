%%

cd('G:\My Drive\Visualization\Data')

files = dir('08_Bubble-Nets_LBAS_00_mn*.mat');

manual_fix = readtable('08_Bubble-Nets_LBAS_02_ALLWHALES_manualsync.xlsx');
strokebubbdata = readtable('08_Bubble-Nets_LBAS_02_ALLWHALES_10Hz_withSRdata.csv');

for kk = 1:length(files)
    
    close all
    
    kk
    W = load(files(kk).name);
    whaledata = table(W.DN(W.tagon),W.pitch(W.tagon),W.roll(W.tagon),W.head(W.tagon),...
        W.Ptrack(W.tagon,1),W.Ptrack(W.tagon,2),W.Ptrack(W.tagon,3),...
        W.geoPtrack(W.tagon,1),W.geoPtrack(W.tagon,2),W.geoPtrack(W.tagon,3),...
        W.p(W.tagon),W.Gw(W.tagon,1),W.Gw(W.tagon,2),W.Gw(W.tagon,3),...
        'VariableNames',{'DN','pitch','roll','head','x','y','z','geo_x','geo_y','geo_z',...
        'Depth','GyrX','GyrY','GyrZ'});
    whaledata.Date_Time = datestr(W.DN(W.tagon),'mm/dd/yyyy HH:MM:SS.fff');
    
    whaledata.head = fillgaps(whaledata.head);
    % Calculate heading change (1st derivative of heading)
    whaledata.headdiff  = [0; diff(whaledata.head)]; 
    
    whaledata.RightSpin = whaledata.headdiff < -pi ; % a right spin past 180 South is a diff of ~ -2*pi
    whaledata.LeftSpin  = whaledata.headdiff > pi ;  % a left spin past 180 South is a diff of ~ +2*pi

    
    % Creating heading column that does not jump between 180 and -180 (for smooth animations)
    % 1. Create cumulative sum of right turns and left turns to keep track of
    % overall turning (past 180 South) to the left or right.
    whaledata.CumulTurns_Rpos = cumsum(whaledata.RightSpin - whaledata.LeftSpin); 
    % 2. Correct heading to add 2*pi to the heading for every right spin past 180 (and
    % subtract 2*pi from the heading for every left spin past 180).
    whaledata.headcorr = whaledata.head + 2*pi*(whaledata.CumulTurns_Rpos);
    % 3. Check that that gets rid of large jumps in heading for smooth animations.
    whaledata.headcorrdiff = [diff(whaledata.headcorr); 0];
    max(whaledata.headcorrdiff)
    
    figure; plot(whaledata.head); hold on; plot(whaledata.headcorr); plot(whaledata.headdiff); plot(whaledata.headcorrdiff)
    
    OrigFileName = extractAfter(files(kk).name,'08_Bubble-Nets_LBAS_00_')
    whaleName = extractBefore(OrigFileName,' 10Hzprh.mat')
    whaledata.whaleName(:) = {whaleName};

    START = datenum('06/14/2021 14:20:00.000','mm/dd/yyyy HH:MM:SS.FFF')
    END = datenum('06/14/2021 14:30:00.000','mm/dd/yyyy HH:MM:SS.FFF')
    whaledata = whaledata(find(whaledata.DN > START & whaledata.DN < END),:);

    datevec(738321.6025)
    LUNGE_DN = 738321.6025;
    [minVal, closestindex] = min(abs(whaledata.DN-LUNGE_DN));
    x_at_lunge = whaledata(closestindex, {'x'});
    y_at_lunge = whaledata(closestindex, {'y'});
    z_at_lunge = whaledata(closestindex, {'z'});
    whaledata.x_fix = whaledata{:,'x'} - x_at_lunge{1,1};
    whaledata.y_fix = whaledata{:,'y'} - y_at_lunge{1,1};
    
    manual_x_fix = manual_fix(find(manual_fix.Animal == kk),'x_fix_10X');
    manual_y_fix = manual_fix(find(manual_fix.Animal == kk),'y_fix_10X');
    
    whaledata.x_finefix = whaledata{:,'x_fix'} + manual_x_fix{1,1};
    whaledata.y_finefix = whaledata{:,'y_fix'} + manual_y_fix{1,1};
    
    figure

    scatter3(whaledata.x,whaledata.y,-whaledata.z);
    hold on
    scatter3(whaledata.x_fix,whaledata.y_fix, -whaledata.z);
    title(strcat(whaleName,' 3D View'))
    print('-painters','-dpng', strcat('08_Bubble-Nets_LBAS_01_',whaleName,'_3D-view.png'))

    figure
    % To check output before saving:
    ax1 = subplot(5,1,[1:2]);
    plot(ax1,whaledata.DN,whaledata.Depth) % plots entire length of processed Depth data
    hold on
    ax1.YDir='reverse';
    ylabel('Depth (m)');
    hold on

    ax2 = subplot(5,1,3);
    plot(ax2, whaledata.DN,whaledata.pitch, whaledata.DN,whaledata.roll)
    ylabel('Pitch & Roll')

    ax3 = subplot(5,1,4);
    plot(ax3, whaledata.DN,whaledata.headcorr)
    ylabel('Heading (rad)')

    ax4 = subplot(5,1,5);
    plot(ax4, whaledata.DN,whaledata.GyrY)
    ylabel('GyrY')

    linkaxes([ax1,ax2,ax3,ax4],'x');
    datetick('x','mmm-dd HH:MM')
    title(strcat(whaleName,' Data View'))
    print('-painters','-dpng', strcat('08_Bubble-Nets_LBAS_01_',whaleName,'_data-view.png'))

    writetable(whaledata,strcat('08_Bubble-Nets_LBAS_01_',whaleName,'_10Hz.csv'));
    whaledata_1hz = downsample(whaledata,10);
    writetable(whaledata,strcat('08_Bubble-Nets_LBAS_01_',whaleName,'_1Hz.csv'));
    
    if kk == 1
        whaledata_1hz_ALL = whaledata_1hz;
        whaledata_ALL = whaledata;
        
    else
        whaledata_1hz_ALL = vertcat(whaledata_1hz_ALL,whaledata_1hz);
        whaledata_ALL = vertcat(whaledata_ALL,whaledata);
    end
end

whaledata_1hz_ALL;
figure
%scatter3(whaledata_1hz_ALL.x_fix,whaledata_1hz_ALL.y_fix, -whaledata_1hz_ALL.z);
hold on
scatter3(whaledata_1hz_ALL.x_finefix,whaledata_1hz_ALL.y_finefix, -whaledata_1hz_ALL.z);

whaledata_ALL.Glide_Controller(:) = strokebubbdata.Glide(1:height(whaledata_ALL));
whaledata_ALL.Stroke_Detected(:) = strokebubbdata.StrokeDetected(1:height(whaledata_ALL));
whaledata_ALL.Bubble_Controller(:) = strokebubbdata.Bubbles(1:height(whaledata_ALL));

writetable(whaledata_1hz_ALL,strcat('08_Bubble-Nets_LBAS_01_ALLWHALES_1Hz.csv'));
writetable(whaledata_ALL,strcat('08_Bubble-Nets_LBAS_01_ALLWHALES_10Hz.csv'));


%% Processing Step 02.F: AFTER RUNNING CATS PRH TOOL

% Must change W.tagon to match decimation factor used in CATS processing
W.tagon = false(size(data.Pressure));
[~,a] = min(abs(DNorig-info.JulDate('ON.ANIMAL')));
[~,b] = min(abs(DNorig-info.JulDate('OFF.ANIMAL')));
W.tagon(a:b) = true;
tagon_dec = downsample(W.tagon,decfac);

% To check output before saving:
ax1 = subplot(5,1,[1:2])
plot(ax1,DN,Depth) % plots entire length of processed Depth data
hold on
plot(ax1,DN(tagon_dec),Depth(tagon_dec)) % plots Depth data from ON.ANIMAL to OFF.ANIMAL - this highlighted section will be exported
ax1.YDir='reverse';
ylabel('Depth (m)');
hold on

ax2 = subplot(5,1,3)
plot(ax2, DN,pitch)
hold on
plot(ax2, DN(tagon_dec),pitch(tagon_dec))
ylabel('Pitch (rad)')

ax3 = subplot(5,1,4)
plot(ax3, DN,roll)
hold on
plot(ax3, DN(tagon_dec),roll(tagon_dec))
ylabel('Roll (rad)')

ax4 = subplot(5,1,5)
plot(ax4, DN,head)
hold on
plot(ax4, DN(tagon_dec),head(tagon_dec))
ylabel('Heading (rad)')

linkaxes([ax1,ax2,ax3,ax4],'x');

% If needed, adjust pitch by a factor of -1 to make sure that descent is
% negative (error might happen randomly based on calibration period selected)
% pitch = -pitch;

%% Save Processed Data 

ProcessedData = table(Aw(tagon_dec,1),Aw(tagon_dec,2),Aw(tagon_dec,3),Mw(tagon_dec,1),Mw(tagon_dec,2),Mw(tagon_dec,3),Gw(tagon_dec,1),Gw(tagon_dec,2),Gw(tagon_dec,3),...
'VariableNames',{'Ax','Ay','Az','Mx','My','Mz','Gx','Gy','Gz'}); %putting all processed data into table
ProcessedData.Depth = Depth(tagon_dec);
ProcessedData.pitch = pitch(tagon_dec);
ProcessedData.roll = roll(tagon_dec);
ProcessedData.heading = head(tagon_dec);
ProcessedData.temp = Temp(tagon_dec);
ProcessedData.illum = Light(tagon_dec);
ProcessedData.W.tagon = W.tagon(tagon_dec);
ProcessedData.Date_Time = datestr(DN(tagon_dec),'mm/dd/yyyy HH:MM:SS.fff');
ProcessedData.JulDateTime = DN(tagon_dec);


% Set data directory; change as necessary.
Data_path='G:\My Drive\Dissertation Sleep\Sleep_Analysis\Data';
cd(Data_path);
PRH_Data= 'G:\My Drive\Dissertation Sleep\Sleep_Analysis\Data\PRH_Data';

s = 13; % PICK A SEAL ID Recording # (see list below)

% See all SealIDs
SealIDs = ["test12_Wednesday",... % Recording 1
    "test20_SnoozySuzy",...       % Recording 2
    "test21_DozyDaisy",...        % Recording 3
    "test23_AshyAshley",...       % Recording 4
    "test24_BerthaBeauty",...     % Recording 5
    "test25_ComaCourtney",...     % Recording 6
    "test26_DreamyDenise",...     % Recording 7
    "test30_ExhaustedEllie",...   % Recording 8
    "test31_FatiguedFiona",...    % Recording 9
    "test32_GoodnightGerty",...   % Recording 10
    "test33_HypoactiveHeidi",...  % Recording 11
    "test34_IndolentIzzy"...       % Recording 12
    "test35_JauntingJuliette"];

writetable(ProcessedData,strcat(SealIDs(s),'_02_Calibrated_Processed_MotionEnvSensors_',num2str(decfac),'Hz_',datestr(ProcessedData.JulDateTime(1),'mmddyy-HHMMSSfff'),'.csv'));

% Save all the random variables you have open in case you need them later
save(strcat(Data_path,'/',SealIDs(s),'_02_Calibrated_Processed_MotionEnvSensors_',num2str(decfac),'Hz_',datestr(ProcessedData.JulDateTime(1),'mmddyy-HHMMSSfff'),'.mat'),...
    'ProcessedData');

%% Optional: Example of how to write data as EDF
ProcessedDataArray = table2array(ProcessedData(:,1:15)).'; 
eeglab
EEG = pop_importdata('dataformat','array','nbchan',0,'data','ProcessedDataArray','srate',5,'pnts',0,'xmin',0);
pop_writeeeg(EEG, 'G:\My Drive\Dissertation Sleep\Sleep_Analysis\Data\FILENAME.edf', 'TYPE','EDF');
eeglab redraw

%% STROKE RATE DETECTION FROM CATS TOOLS

% Tailbeat detect in CATS tools: https://github.com/wgough/CATS-Methods-Materials/blob/master/CATSMatlabTools/Other%20tag%20tools/TailbeatDetect.m

