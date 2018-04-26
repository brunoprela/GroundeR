function [pos_all, best_box] = getPosp( proposals, ground_truth)
    pos_all = [];
    best = 0;
    best_box = [];
    [m, n] = size(proposals);
    for i = 1:numel(m)
        % note that we record the corresponding row of the box
        cur = proposals(i, :);
        temp = get_iou(cur, ground_truth);
        if temp > 0.5
            pos_all = [pos_all, i];
            if temp > best
                best = temp;
                best_box = i;
            end
        end 
    end
    if best == 0
        best_box = -1;
    end
end

function iou = get_iou(b1, b2)
    xmin = np.max(b1{0}, b2{0});
	ymin = np.max(b1{1}, b2{1});
	xmax = np.min(b1{2}, b2{2});
	ymax = np.min(b1{3}, b2{3});

	intersection = get_area(xmax - xmin, ymax - ymin);
	union = get_area(b1{2} - b1{0}, b1{3} - b1{1}) + get_area(b2{2} - b2{0}, b2{3} - b2{1}) - intersection;
	iou = intersection / union;
end

function area = get_area(w, h)
    area = w * h;
end
