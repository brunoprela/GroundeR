fn1 = './Flickr30kEntities/Annotations/6609688031.xml' ;
fn2 = './Flickr30kEntities/Sentences/6609688031.txt';
Ann = getAnnotations(fn1);
Sen = getSentenceData(fn2);
queryList = {};

%get list of all query: get all phrases listed in flicker
for i = 1:numel(Sen)
        temp = Sen(i).phraseID;
        for j = 1:numel(temp)
            queryList = [queryList, temp(j)];
        end
end

disp(queryList)

%find mapping for all phrases 
for i = 1:numel(Ann.id)
    %getBox
    box = 
    %getwordID sequences for this phrase
    
    %compute all positive prosoal
    
    %get best proposal
    
   
end