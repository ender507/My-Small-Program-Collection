%构造信号
dt = 0.01;
t = -2*pi:dt:2*pi;
ft = (1+cos(t))/2 .*(t>=-pi&t<=pi);
% 打印波形
subplot(5,3,1),plot(t,ft);
ylabel('f(t)');
axis([-1.5*pi,1.5*pi,1.1*min(ft),1.1*max(ft)]);
title('信号波形');
grid on;
% 打印频谱
N = length(t);
k = -N/2:N/2;
w = k * 12 * pi / N;                       %频谱范围:-6pi到6pi
F= ft * exp(-j * t' * w) * dt;            %对原信号进行傅里叶变换
subplot(6,3,3),plot(w,abs(F));
axis([-pi,pi,min(abs(F))-0.2,1.1*max(abs(F))])
title('频谱');
ylabel('F(jw)');
grid on;
%针对不同的采样周期进行采样
for i = 1:3
	%三种情况下不同的采样周期
	if i==1
        Ts = 1;
	elseif i==2
    	Ts = pi/2;
	else Ts = 2;
    end
	n = -100*pi:Ts:100*pi;              %采样点
	f = (1+cos(n))/2.*(n>=-pi&n<=pi);   %原信号进行采样并输出
	subplot(6,3,i+3),stem(n,f,'filled');
    axis([-1.5*pi,1.5*pi,1.1*min(f),1.1*max(f)]);
	str = ['采样周期为',num2str(Ts),'的采样信号'];
    title(str);
    ylabel('fp(n)');
    grid on;
    N = length(n);
    k = -N/2:N/2;
    w = k * 6 * pi / N;                       %频谱范围:-3pi到3pi
    F= f * exp(-j * n' * w) * Ts;            %对采样信号进行傅里叶变换
    subplot(6,3,i+6),plot(w,abs(F));
    axis([min(w),max(w),min(abs(F))-0.2,1.1*max(abs(F))]);
    str = ['采样周期为',num2str(Ts),'的频谱'];
    title(str);
    ylabel('Fp(jw)');
    grid on;
    
    if Ts==pi/2     % Ts==pi/2时不讨论重建
        continue;
    end
    
    %重建
    wc = 2.4;
    %内插公式
    fr = f/pi*Ts*wc*sinc((wc/pi)*(ones(length(n),1)*t - n'*ones(1,length(t))));
    subplot(6,3,i+9),plot(t,fr); 
    axis([-1.5*pi,1.5*pi,1.1*min(fr),1.1*max(fr)]);
    str = ['采样周期为',num2str(Ts),'的重建信号'];
    title(str);
    grid on;
    
    N = length(t);
    k = -N/2:N/2-1;
    w = k * 12 * pi / N;                       %频谱范围:-6pi到6pi
    Fr= fr * exp(-j * t' * w) * dt;            %对fr信号进行傅里叶变换
    subplot(6,3,i+12),plot(w,abs(Fr));
    axis([-pi,pi,min(abs(Fr))-0.2,1.1*max(abs(Fr))])
    str = ['采样周期为',num2str(Ts),'的重建信号频谱'];
    title(str);
    ylabel('Fr(jw)');
    grid on;
    
    subplot(6,3,i+15),plot(t,abs(fr-ft));
    axis([-1.5*pi,1.5*pi,-0.01,1.1*max(abs(fr-ft))]);
    str = ['采样周期为',num2str(Ts),'的绝对误差'];
    title(str);
    grid on;
end
