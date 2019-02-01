w = [];
for i = 1:16
    t = time(idx==i);
    w = [w;mean(t)];
end
