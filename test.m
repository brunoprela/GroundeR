% fn = '';
% if ~exist(fn,'file')
%         error('file not found');
% end
% fid = fopen(fn, 'rt');
% while true
%     curline = fgetl(fid);
%     if ~ischar(curline)
%         break;
%     end
%     fn1 = strcat('./Flickr30kEntities/Annotations/',curline, '.xml') ;
%     fn2 = strcat('./Flickr30kEntities/Sentences/',curline, '.txt') ;
%     fn3 = strcat('./flickr30k_img_bbx_ss/', curline, '.mat');

files = dir('./Flickr30kEntities/Annotations/*.xml');
% for f = files'
%     curline = f.name(1:end-4);
%     disp(curline);
%     fn1 = strcat('./Flickr30kEntities/Annotations/',curline, '.xml') ;
%     fn2 = strcat('./Flickr30kEntities/Sentences/',curline, '.txt') ;
%     fn3 = strcat('./flickr30k_img_bbx_ss/', curline, '.mat');
%     
    

    fn1 = './Flickr30kEntities/Annotations/2612125121.xml' ;
    fn2 = './Flickr30kEntities/Sentences/2612125121.txt';
    fn3 = './flickr30k_img_bbx_ss/2612125121.mat';
    curline = '2612125121;';

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
        pcount = 0;
        wordID = [];
        for j = 1:numel(Sen)
            temp = Sen(j).phraseID;
            for k = 1:numel(temp)
                disp(curline)
                disp(size(temp{k}))
                disp(size(Ann.id{i}))
                disp(temp{k})
                disp(Ann.id{i})
                if eq(str2double(temp{k}), str2double(Ann.id{i})) 
                    pcount = pcount + 1;
                    if isempty(wordID)
                        wordID = Sen(j).phrases(k);
                    end
                end
            end
        end

        %getBox if multiple chose first one

        %disp(Ann.id{i})
        boxindex = Ann.idToLabel(i);
        [m, n] = size(boxindex{1});
        if m > 1
            for j = 1:m
                curLabel = Ann.labels(boxindex{1}(j, 1));
                box = curLabel.boxes;
                %nobox = curLabel.nobox;
                %[a, b] = size(box)
                %disp(isempty(nobox));
                if isempty(curLabel.scene) && isempty(curLabel.nobox)
                    [prop_list, best_box] = getPosp(proposals_matrix, box);
                else
                    if ~isempty(curLabel.scene)
                        if ~isempty(curLabel.nobox)
                            disp(curline)
                        else 
                            xmax = Ann.dims{1};
                            ymax = Ann.dims{2};
                            box = [0, 0, xmax, ymax];
                            [prop_list, best_box] = getPosp(proposals_matrix, box);
                        end
                    else
                        box = [0, 0, 0, 0];
                        prop_list = [-1];
                        best_box = [-1];
                    end
                 
%                     if curLabel.scene == 1 && curLabel.nobox == 1
%                         disp(curline);
%                     end
%                     if curLabel.scene == 0 && curLabel.nobox == 0
%                         disp(curline);
%                     end
%                    
%                     if curLabel.scene == 1
%                         xmax = Ann.dims{1};
%                         ymax = Ann.dims{2};
%                         box = [0, 0, xmax, ymax];
%                         [prop_list, best_box] = getPosp(proposals_matrix, box);
%                     elseif curLabel.nobox == 1
%                     %for when there's no box
%                         box = [0, 0, 0, 0];
%                         prop_list = [-1];
%                         best_box = [-1];
%                     end
                end
                for t = 1:pcount
                    queryList = [queryList, Ann.id{i}];
                    boxList = [boxList, box];
                    propList = [propList, prop_list];
                    propidList = [propidList, best_box];
                    wordList = [wordList, wordID]
                %disp(prop_list)
                end
            end
        else 

            curLabel = Ann.labels(boxindex{1}(1, 1));
            box = curLabel.boxes;

            %box = Ann.labels(boxindex{1}).boxes;

            %[a, b] = size(box)
            if isempty(curLabel.scene) && isempty(curLabel.nobox)
                    [prop_list, best_box] = getPosp(proposals_matrix, box);
            else
                if ~isempty(curLabel.scene)
                    if ~isempty(curLabel.nobox)
                        disp(curline)
                    else 
                        xmax = Ann.dims{1};
                        ymax = Ann.dims{2};
                        box = [0, 0, xmax, ymax];
                        [prop_list, best_box] = getPosp(proposals_matrix, box);
                    end
                else
                    box = [0, 0, 0, 0];
                    prop_list = [-1];
                    best_box = [-1];
                end

%                     if curLabel.scene == 1 && curLabel.nobox == 1
%                         disp(curline);
%                     end
%                     if curLabel.scene == 0 && curLabel.nobox == 0
%                         disp(curline);
%                     end
%                    
%                     if curLabel.scene == 1
%                         xmax = Ann.dims{1};
%                         ymax = Ann.dims{2};
%                         box = [0, 0, xmax, ymax];
%                         [prop_list, best_box] = getPosp(proposals_matrix, box);
%                     elseif curLabel.nobox == 1
%                     %for when there's no box
%                         box = [0, 0, 0, 0];
%                         prop_list = [-1];
%                         best_box = [-1];
%                     end
            end
            for t = 1:pcount
                queryList = [queryList, Ann.id{i}];
                boxList = [boxList, box];    
                %[prop_list, best_box] = getPosp(proposals_matrix, box);
                propList = [propList, prop_list]
                propidList = [propidList, best_box]
                wordList = [wordList, wordID]
            end

        end
        %getwordID sequences for this phrase (now those are just words)
%         wordID = [];
%         for j = 1:numel(Sen)
%             temp = Sen(j).phraseID;
%             for k = 1:numel(temp)
%                 if and((temp{k} == Ann.id{i}),(isempty(wordID))) 
%                     wordID = Sen(j).phrases(k);
%                 end
%             end
%         end
% 
%         for j = 1:m
%             wordList = [wordList, wordID]
%         end
    end
    temp = strcat('./annotation/', curline, '.mat');
    save(temp, 'queryList', 'boxList', 'wordList', 'propList', 'propidList');
%end
 