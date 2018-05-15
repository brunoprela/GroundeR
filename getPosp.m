function [pos_all, best_box] = getPosp( proposals, ground_truth)
        pos_all = [];
        best = 0;
        count = 0;
        best_box = -1;
        [a, b] = size(ground_truth);
        
        [m, n] = size(proposals);
        for i = 1:m
            %disp(i)
            % note that we record the corresponding row of the box
            cur = proposals(i, :);
            temp = get_iou(cur, ground_truth);
            %disp(temp);

            if temp >= 0.4
                pos_all = [pos_all, i];
                count = count + 1;
                if temp > best
                    best = temp;
                    best_box = count;
                end
            end 
        end
        if isempty(pos_all)
            pos_all = [-2];
        end
        
end

function iou = get_iou(b1, b2)
    xmin = max(b1(1), b2(1));
	ymin = max(b1(2), b2(2));
	xmax = min(b1(3), b2(3));
	ymax = min(b1(4), b2(4));

	intersection = get_area(xmax - xmin, ymax - ymin);
	union = get_area(b1(3) - b1(1), b1(4) - b1(2)) + get_area(b2(3) - b2(1), b2(4) - b2(2)) - intersection;
	iou = intersection / union;
end

function area = get_area(w, h)
    area = (w + 1) * (h + 1);
end
