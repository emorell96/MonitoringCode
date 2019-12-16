function waterInterlock_LI_v8()
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%interlock.m
%Version v8
%Last Modified: 2019/10/11
%Authors: Cora Fujiwara & Max Prichard
%This MATLAB code is meant to manage the interlock system on the water
%cooling system.  It interfaces with an arduino which takes measurements of
%the temperature and flow rates through the various magnets in the
%experiment. 

% v8 Update : This is meant to run on GOB and not to be compiled
%% DEFAULTS SETTINGS
LI_COM='COM14';
numPoints=30;
updatePeriod=0.5;
timeLimits=[0 30];
tempLimits=[15 40];
flowLimits=[0 5]; 
li_ch=[0,1,2,3,4,5,6,7,8];
temp_hp=45;
temp_lp=15;
flow_lp = 3;
li_lg_str={'Ch 0','Ch 1','Ch 2','Ch 3','Ch 4','Ch 5','Ch 6','Ch 7','Ch8'};
li_flow_str = {'Ch 0','Ch 1','Ch 2','Ch 3','Ch 4','Ch 5','Ch 6','Ch 7'};
readTime=0.5;
ALARM=0;

%% LOAD SETTINGS
cl_list={'r','b','g','c','k','m'};
mk_list={'o','+'};
LI_COM='COM14';
numPoints=30;
updatePeriod=1;
timeLimits=[0 35];
tempLimits=[15 40];

temp_hp=45;
temp_lp=15;
flow_lp = 2.5;
flowLimits = [0 5];


li_lg_str={'Ch0 Total Flow Return','Ch1 ZS D','Ch3 TOP MOT Inner','Ch4 TOT IN','Ch 5 BOT MOT Outer','Ch6 ZS A','Ch7 TOP MOT Outer','Ch8 ZS B'};
li_ch=[0,1,3,4,5,6,7,8];
li_flow_str={'TOP MOT 3,4 OUT','BOT MOT 3,4 OUT','BOT MOT 1,2 OUT','TOT OUT','ZS B 1,2 OUT','TOT IN','ZS A 1,2 + ZS D OUT','TOP MOT 1,2 OUT'};

disp('Loading config.txt....');
eval(fileread('config.txt'))

%% Stuff
li_chnum=length(li_ch);
li_flownum = length(li_flow_str);
li_plts=cell(li_chnum);
li_flows = cell(li_flownum);
dataCounter=1;

%% Establish Connection
try
    delete(instrfind('Port',LI_COM));
    sLi=establishConnection(LI_COM);
    
    while(sLi.BytesAvailable>0)
        fread(sLi,sLi.BytesAvailable);
    end
    pause(0.5);
catch
    delete((instrfind('Port',LI_COM)));
    error('Could not connect to Arduinos.');     
end


%% RUN GUI
try       
    updateTimer=timer('Period', updatePeriod, ...
        'ExecutionMode', 'fixedSpacing', ...
        'TimerFcn', @callbackUpdateTimer);    
    gui=figure(10101010);%Initialize figure
    
    timeVector=zeros(numPoints,1);   
    set(gui, 'MenuBar', 'none','ToolBar','none','Color','w',...
        'Name','Water Temperature Monitor','NumberTitle','Off',...
        'Resize','off');  
    set(gui,'Position', [100 100 950 600]);
    set(gui, 'CloseRequestFcn', @closeGUI);
    
    %% LITHIUM TEMP DATA
    li_ax1=subplot(2,1,1);
    li_ax1.Units='pixels';
   
    
    hold on
    for kk=1:li_chnum
        li_plts{kk}=scatter(li_ax1,zeros(numPoints,1),zeros(numPoints,1));
        li_plts{kk}.Marker=mk_list{floor(kk/length(cl_list))+1};        
        li_plts{kk}.MarkerFaceColor=cl_list{mod(kk,length(cl_list))+1};
        li_plts{kk}.MarkerEdgeColor=cl_list{mod(kk,length(cl_list))+1};    
    end    
    li_lg=legend(li_ax1,li_lg_str,'FontSize',8,'Location','northeastoutside'); 

    set(li_ax1, 'FontSize', 12);
    set(li_ax1,'XMinorTick','on','YMinorTick','on','XMinorGrid','on',...
        'XGrid','On', 'YGrid', 'On', 'YMinorGrid','On','Box','On');   
    xlabel(li_ax1,'Time Ago (s)'); 
    ylabel(li_ax1,'Temperature (C)'); 
    xlim(li_ax1,timeLimits);
    ylim(li_ax1, tempLimits);
    title('Li Water Temperature');    
    
    li_ax1.Position(1)=45;
    li_ax1.Position(2)=345;
    li_ax1.Position(3)=gui.Position(3)-300;
    li_ax1.Position(4)=gui.Position(4)-375;
    
    li_lg.Units='pixels';
    li_lg.Position(3)=200;
    li_lg.Position(4)=15*li_chnum;
    li_lg.Position(1)=li_ax1.Position(1)+li_ax1.Position(3)+10;
    li_lg.Position(2)=gui.Position(4)-li_lg.Position(4)-32;
    
    %%Lithium Flow Data
    
    li_ax2=subplot(2,1,2);
    li_ax2.Units='pixels';
    
    hold on
    for kk=1:li_flownum
        li_flows{kk}=scatter(li_ax2,zeros(numPoints,1),zeros(numPoints,1));
        li_flows{kk}.Marker=mk_list{floor(kk/length(cl_list))+1};        
        li_flows{kk}.MarkerFaceColor=cl_list{mod(kk,length(cl_list))+1};
        li_flows{kk}.MarkerEdgeColor=cl_list{mod(kk,length(cl_list))+1};    
    end    
    flow_lg =legend(li_ax2,li_flow_str,'FontSize',8,'Location','northeastoutside'); 

    set(li_ax2, 'FontSize', 12);
    set(li_ax2,'XMinorTick','on','YMinorTick','on','XMinorGrid','on',...
        'XGrid','On', 'YGrid', 'On', 'YMinorGrid','On','Box','On');   
    xlabel(li_ax2,'Time Ago (s)'); 
    xlim(li_ax2,timeLimits);
    ylabel(li_ax2,'Flow Rate (V)'); 
    ylim(li_ax2, flowLimits);
%     yyaxis right;
%     ylabel(li_ax2,'Flow Rate (L/min)');
%     ylim(li_ax2,flowLimits_L); Not all flow rates necessarily correspond.
    title('Li Flow Rates');
    
%     li_ax2.YAxis(1).Color='k';
%     li_ax2.YAxis(2).Color='k';

    li_ax2.Position(1)=45;
    li_ax2.Position(2)=50;
    li_ax2.Position(3)=gui.Position(3)-300;
    li_ax2.Position(4)=gui.Position(4)-375;
    
    flow_lg.Units='pixels';
    flow_lg.Position(3)=150;
    flow_lg.Position(4)=15*li_flownum;
    flow_lg.Position(1)=li_ax2.Position(1)+li_ax2.Position(3)+60;
    flow_lg.Position(2)=gui.Position(4)-flow_lg.Position(4)-332;
    
%     flowBox=annotation('textbox','units','pixels','FontSize',10);
%     flowBox.Position(1)=li_ax1.Position(1)+li_ax1.Position(3)+80;
%     flowBox.Position(3)=120;
%     flowBox.Position(2)=90;
%     flowBox.Position(4)=40;
%     flowBox.String=sprintf(['Inlet : \nOutlet :']) ;
  
    %% FINISH        
    disp('Starting timer...');
    pause(1);    
    if sLi.BytesAvailable
        fread(sLi,sLi.BytesAvailable);
    end
    timeVector=now*ones(numPoints,1);
    start(updateTimer);
    disp('Showing GUI...');    
   
catch exception
    disp('Exception Found! COM closed. Display closed.')
    stop(updateTimer);
    delete(instrfind('Port',LI_COM));
    delete(gui);
    throw(exception);
end

function closeGUI(~,~)
    disp('Closing the GUI...');
    stop(updateTimer);
    pause(2);
    delete(instrfind('Port',LI_COM));
    delete(gui);
    disp('Done!');
end

function callbackUpdateTimer(~,~)
    timeVector(dataCounter)=now;
    pltTimeVector=(now-timeVector)*25*3600;     
	
	% flush the serial buffer
    if sLi.BytesAvailable
        fread(sLi,sLi.BytesAvailable);
    end  
	
	
	% Send a carriage return or linefeed
    fwrite(sLi,13);   
	
	% Wait for arduino to update its temperature and spit them back out
    pause(readTime);  
    
	% Read the data if it's available
    if sLi.BytesAvailable    
        outputLi=fread(sLi,sLi.BytesAvailable);      % Read Data
    else
        disp([datestr(now,13) ' No response from device.']);
        outputLi=0;
    end
    

	% Check that the arduino sent you the correct number of bytes
    if (length(outputLi)~=48)                % Check for errors
       return 
    end
    
	% Convert temperature bytes to temperature
   temps=bin2dec([dec2bin(outputLi(1:2:end),8) ...  
        dec2bin(outputLi(2:2:end),8)]);
    temps=2.5586*(temps*0.1875/2.5-100);
    temps=temps(li_ch+1);                            % Get desired ch's
    % Convert to temps [b0 b1 b2 b3 b4 b5 ....]
	% T1=[b0 b1] = [0,65535] then convert that number to a voltage and then use the current source circuit to convert to temperature
    
	% Do the same thing to the flow meters
    flows = bin2dec([dec2bin(outputLi(33:2:end),8) ...  % Get the reading, 
        dec2bin(outputLi(34:2:end),8)]);                 %Then convert to volts (Arduino is 10 bit)
    flows = flows/1023*5;

    if (sum((temps>temp_hp)+(temps<temp_lp))...
            +sum(flows<flow_lp))~=0
        set(gui,'Color','Red');
        ALARM=1;
    else
        if ALARM                                     % Unset alarm
            set(gui,'Color','white');
        end
    end
    for ii=1:li_chnum  
        li_lg.String{ii}=[li_lg_str{ii} ': '...
            sprintf('%.2f',temps(ii))];
        li_plts{ii}.XData=pltTimeVector;
        li_plts{ii}.YData(dataCounter)=temps(ii); 
    end       
    for ii = 1:li_flownum
        flow_lg.String{ii}=[li_flow_str{ii} ': '...
            sprintf('%.2f',flows(ii)) ' V'];
        li_flows{ii}.XData=pltTimeVector;
        li_flows{ii}.YData(dataCounter)=flows(ii);
    end
    

%     flowBox.String=sprintf(['Inlet    : ' num2str(INFLOW,3) 'V\nOutlet : '...
%         num2str(OUTFLOW,3) 'V']) ;
    drawnow;
    
    if mod(dataCounter,numPoints)==0
       dataCounter=1;
    else
        dataCounter=dataCounter+1;
    end   
end

end


function s=establishConnection(COM)
    port=COM;
    baud=9600;
    databits=8;
    stopbits=1;
    parity='none';
    flowcontrol='none';
    s=serial(port,'BaudRate',baud,...
        'Parity',parity,'StopBits',...
        stopbits,'DataBits',databits,'FlowControl',flowcontrol);
    set(s,'terminator','CR');

    fopen(s);
    disp('Connection has been establishied.');
end

