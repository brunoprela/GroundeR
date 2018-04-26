fn1 = './Flickr30kEntities/Annotations/6609688031.xml' ;
fn2 = './Flickr30kEntities/Sentences/6609688031.txt';
Ann = getAnnotations(fn1);
Sen = getSentenceData(fn2);


queryList = [];
boxList = [];
wordList = [];

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
    boxindex = Ann.idToLabel(i);
    index = 0;
    if length(boxindex) > 1
        for j = 1:numel(boxindex)
            append(queryList, Ann.id(i));
            append(boxList, boxindex(j));
        end
    else 
        append(queryList, Ann.id(i));
        append(boxList, boxindex);
    end
    box = Ann.labels(index);
    %getwordID sequences for this phrase (now those are just words)
    wordID = [];
    for j = 1:numel(Sen)
        temp = Sen(j).phraseID;
        for k = 1:numel(temp)
            if temp(k) == Ann.id(i) and length(wordID) == 0 
                wordID = Sen(j).phrases(k);
            end
        end
    end
    
    for j = 1:numel(boxindex)
        append(wordList, wordID)
    end
end