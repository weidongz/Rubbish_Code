function [HashResult, distance] = rank_show( FilePath, HashTable )
% this function is used to count hamming distance and return the sorted 3
% similar pictures filename
% input: FilePath:the requiry image fullfilename
%        HashTable: the method you  used to retrivel
% output : HashResult:the top 3 smallest hamming distance pic photo name
%          distance: the top 3 smallest hamming distance

if HashTable == 'ahash'
    load AHashResult.mat AHashResult
    PicData = imread(FilePath);
    AHashData = get_ahash_value(PicData);
    dist = [];
    for i=1:size(AHashResult,2)
        dist(i,1) = sum(bitxor(AHashResult{1,i},AHashData));%Hamming distance
        [dist1,index] = sort(dist(:,1));
    end
    distance = [dist1(1), dist1(2), dist1(3)];
    HashResult = {AHashResult{3,index(1)};AHashResult{3,index(2)};AHashResult{3,index(3)}};


elseif HashTable == 'phash'
    load PHashTable.mat PHashTable
    PicData = imread(FilePath);
    PHashData = get_phash_value(PicData);
    dist = [];
    for i=1:size(PHashTable,2)
        dist(i,1) = sum(bitxor(PHashTable{1,i},PHashData));%Hamming distance
        [dist1,index] = sort(dist(:,1));
    end
    distance = [dist1(1), dist1(2), dist1(3)];
    HashResult = {PHashTable{3,index(1)};PHashTable{3,index(2)};PHashTable{3,index(3)}};


elseif HashTable == 'dhash'
    load DHashTable.mat DHashTable
    PicData = imread(FilePath);
    DHashData = get_dhash_value(PicData);
    dist = [];
    for i=1:size(DHashTable,2)
        dist(i,1) = sum(bitxor(DHashTable{1,i},DHashData));%Hamming distance
        [dist1,index] = sort(dist(:,1));
    end
    distance = [dist1(1), dist1(2), dist1(3)];
    HashResult = {DHashTable{3,index(1)};DHashTable{3,index(2)};DHashTable{3,index(3)}};

else
    error('wronginput');
end

end