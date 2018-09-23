function [dx,y] = DCMotor(t,x,u,c,k,varargin)
dx = [ x(2);
    ((-c)*x(2)+(k)*u(1))];
y = x(1);
end