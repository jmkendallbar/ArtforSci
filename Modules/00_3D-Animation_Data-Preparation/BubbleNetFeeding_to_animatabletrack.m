cd('G:\My Drive\Visualization\Data')

load('08_Bubble-Nets_LBAS_00_SingleBubbleNetFeedingDives_mn190718-42 10Hzprh.mat')
whaledata = table(pitch,roll,head,GPS,Ptrack,geoPtrack,p,Gw(:,1),tagon);

figure

scatter3(geoPtrack(:,1),geoPtrack(:,2),geoPtrack(:,3));
