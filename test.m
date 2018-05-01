fn = '';
if ~exist(fn,'file')
        error('file not found');
end
fid = fopen(fn, 'rt');
while true
    curline = fgetl(fid);
    if ~ischar(curline)
        break;
    end
    fn1 = strcat('./Flickr30kEntities/Annotations/',curline, '.xml') ;
    fn2 = strcat('./Flickr30kEntities/Sentences/',curline, '.txt') ;
    fn3 = strcat('./flickr30k_img_bbx_ss/', curline, '.mat');


%fn1 = './Flickr30kEntities/Annotations/6609688031.xml' ;
%fn2 = './Flickr30kEntities/Sentences/6609688031.txt';
%fn3 = './flickr30k_img_bbx_ss/6609688031.mat';

    Ann = getAnnotations(fn1);
    Sen = getSentenceData(fn2);

    proposals = load(fn3);
    proposals_matrix = proposals.cur_bbxes;

    queryList = {};
    boxList = {};
    wordList = {};
    propList = {};
    propidList = {};
    %get list of all query: get all phrases listed in flicker
    %this has a lot of repetetion.
    % for i = 1:numel(Sen)
    %         temp = Sen(i).phraseID;
    %         for j = 1:numel(temp)
    %             queryList = [queryList, temp(j)];
    %         end
    % end

    %find mapping for all phrases 
    %all this is not stored
    for i = 1:numel(Ann.id)
        %getBox if multiple chose first one

        %disp(Ann.id{i})
        boxindex = Ann.idToLabel(i);
        [m, n] = size(boxindex{1});
        if m > 1
            for j = 1:m
                curLabel = Ann.labels(boxindex{1}(j, 1));
                box = curLabel.boxes;

                %[a, b] = size(box)
                if curLabel.nobox == 0
                    [prop_list, best_box] = getPosp(proposals_matrix, box);
                else
                    %for when there's no box
                    box = [0, 0, 0, 0];
                    prop_list = [];
                    best_box = [-1];
                end
                queryList = [queryList, Ann.id{i}];
                boxList = [boxList, box];
                propList = [propList, prop_list]
                propidList = [propidList, best_box]
                %disp(prop_list)
            end
        else 

            curLabel = Ann.labels(boxindex{1}(j, 1));
            box = curLabel.boxes;

            %box = Ann.labels(boxindex{1}).boxes;

            %[a, b] = size(box)
            if curLabel.nobox == 0

                [prop_list, best_box] = getPosp(proposals_matrix, box);
            else

                box = [0, 0, 0, 0];
                prop_list = [];
                best_box = [-1];
            end
            queryList = [queryList, Ann.id{i}];
            boxList = [boxList, box];    
            %[prop_list, best_box] = getPosp(proposals_matrix, box);
            propList = [propList, prop_list]
            propidList = [propidList, best_box]

        end
        %getwordID sequences for this phrase (now those are just words)
        wordID = [];
        for j = 1:numel(Sen)
            temp = Sen(j).phraseID;
            for k = 1:numel(temp)
                if and((temp{k} == Ann.id{i}),(isempty(wordID))) 
                    wordID = Sen(j).phrases(k);
                end
            end
        end

        for j = 1:numel(boxindex)
            wordList = [wordList, wordID]
        end
    end
    filename = strcat('./annotation/', curline, '.mat');
    save(filename, queryList, boxList, wordList, propList, propidList);
end
 