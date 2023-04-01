function preprocessing(source_path, destination_path)
    files = dir(fullfile(source_path));
    files=files(~ismember({files.name},{'.','..'}));

    if ~exist(destination_path, 'dir')
       mkdir(destination_path)
    end
    
    for i = 1:length(files)
        file_path = fullfile(source_path,files(i).name);
    
        [y, Fs] = audioread(file_path);
    
        n = length(y); 
        duration = n/Fs;
        t = linspace(0, duration, n);
        y_r = resample(y,t, 4096);
    
        [pathstr, name, ext] = fileparts(file_path);
        filename = fullfile(destination_path, sprintf('%s.txt', name));
    
        table = array2table(y_r);
        table.Properties.VariableNames(1:2) = {'needle','surface'};
        writetable(table, sprintf(filename, name) )
    end
end
