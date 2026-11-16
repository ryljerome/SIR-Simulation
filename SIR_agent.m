clear; 
close all;

warning('off','all')


N=300; NN=1;                                % total number of S and I people; 
T=100;                                      % number of days
L=100; ll=3;                                % length and width of the domain
gamma=0.1; beta=0.2;                        % rates of recovery and infection
D=0.5; Di=0;                                % rates of movement of healthy and infected
delta=3;                                    % contact radius
x=L*rand(N,1); y=ll*rand(N,1);              % initial xy coords of Susceptible 
% average inter-personal distance = 1
ix=1;iy=1;                                  % initial xy coords of Infected
rx=[];ry=[];                                % initial xy coords of Recovered
NS=(1:T); NI=(1:T); NR=(1:T);               % numbers of S,I,R as function of time
F(T) = struct('cdata',[],'colormap',[]);    % for making movie
 
for j = 1:T
    
    rec = []; 

    % indices of Recovered
    for k = 1:length(ix) % recovery of infected loop
        if rand < gamma % recovery as a random event with rate gamma
            rec = [rec k]; % adding a Recovered
        else rec = rec; 
        end 
    end
    rx = [rx; ix(rec)]; ry = [ry; iy(rec)]; ix(rec) = []; iy(rec) = []; 
    % updating coordinates of I and R
            
    dist=(1:length(ix)); % vector of S-I distances;
    inf=[];
    
    % indices of Infected
    for kk = 1:length(x) % infection loop, going through S people
        for k = 1:length(ix) % going through I people
            dist(k) = sqrt((ix(k)-x(kk))^2+(iy(k)-y(kk))^2); % S-I dist 
            d = min(dist); 
        end % minimal S-I dist
        if d < delta && rand < beta 
            inf=[inf kk]; % infection event
        else inf=inf; 
        end
    end
     
    ix = [ix; x(inf)]; iy = [iy; y(inf)]; x(inf) = []; y(inf) = [];
    % updating coordinates of I and S
    
    % movement of S
    for k=1:length(x) 
        if x(k)<0 
            x(k)=0; 
        elseif x(k)>L 
            x(k)=L; % boundary conditions
        elseif y(k)<0 
            y(k)=0; 
        elseif y(k)>ll 
            y(k)=ll; 
        else
            x(k)=x(k)+D*randn; y(k)=y(k)+D*randn; 
        end
    end
    
    % random step
    for k=1:length(ix) % movement of I
        if ix(k)<0 
            ix(k)=0; 
        elseif ix(k)>L 
            ix(k)=L;  % boundary conditions
        elseif iy(k)<0 
            iy(k)=0; 
        elseif iy(k)>ll 
            iy(k)=ll; 
        else
            ix(k)=ix(k)+Di*randn; iy(k)=iy(k)+Di*randn; 
        end
    end % rand step

    for k=1:length(rx) % movement of R
        if rx(k)<0 
            rx(k)=0; 
        elseif rx(k)>L 
            rx(k)=L;  % boundary conditions
        elseif ry(k)<0 
            ry(k)=0; 
        elseif ry(k)>ll 
            ry(k)=ll; 
        else
            rx(k)=rx(k)+D*randn; ry(k)=ry(k)+D*randn; 
        end 
    end % random step

    %figure(j)
    NS(j)=length(x); NI(j)=length(ix); NR(j)=length(rx); 
    plot(x,y,'.b',ix,iy,'*r',rx,ry,'o g'), axis([-1 L+1 -1 ll+1]);
    pbaspect([5 1 1]);
    set(gca,'FontSize',20,'FontName','Times');
    set(gcf,'color','w');
    legend('Susceptible','Infected','Recovered');
    F(j) = getframe(gcf); % for making movie
end
 
plot((1:T),NS,'b',(1:T),NI,'r',(1:T),NR,'g','LineWidth',2);
ylabel('Number of individuals'); xlabel('Time');
legend('Susceptible','Infected','Recovered');
set(gca,'FontSize',20,'FontName','Times');
set(gcf,'color','w');