fn1 = './Flickr30kEntities/Annotations/6609688031.xml' ;
fn2 = './Flickr30kEntities/Sentences/6609688031.txt';
Ann = getAnnotations(fn1);
Sen = getSentenceData(fn2);
queryList = {};

%get list of all query: get all phrases listed in flicker
%this has a lot of repetetion.
for i = 1:numel(Sen)
        temp = Sen(i).phraseID;
        for j = 1:numel(temp)
            queryList = [queryList, temp(j)];
        end
end

disp(queryList)

%find mapping for all phrases 
%all this is not stored
for i = 1:numel(Ann.id)
    %getBox
    boxindex = Ann.idToLabel(i);
    index = 0;
    if length(boxindex) > 1
        index = boxindex(1);
    else 
        index = boxindex;
    end
    box = Ann.labels(index);
    %getwordID sequences for this phrase (now those are just words)
    wordID = [];
    for j = 1:numel(Sen)
        temp = Sen(j).phraseID;
        for k = 1:numel(temp)
            if temp(k) == Ann.id(i)
                wordID = Sen(j).phrases(k);
            end
        end
    end
end