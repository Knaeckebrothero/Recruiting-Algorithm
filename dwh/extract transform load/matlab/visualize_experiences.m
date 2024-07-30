% Extract all experiences
all_experiences = {};
for i = 1:length(collection)
    if isfield(collection(i), 'experiences') && ~isempty(collection(i).experiences)
        all_experiences = [all_experiences, collection(i).experiences];
    end
end

% 1. Distribution of experience durations
durations = [];
for i = 1:length(all_experiences)
    exp = all_experiences{i};
    if isfield(exp, 'starts_at') && ~isempty(exp.starts_at)
        if isfield(exp, 'ends_at') && ~isempty(exp.ends_at)
            durations = [durations, calcDuration(exp.starts_at, exp.ends_at)];
        else
            durations = [durations, calcDuration(exp.starts_at, [])];
        end
    end
end

% Cap durations at 400 months
durations(durations > 400) = 400;

figure;
h = histogram(durations, 40);  % Increase number of bins for more detail
title('Distribution of Experience Durations');
xlabel('Duration (months)');
ylabel('Count');
xlim([0 400]);

% Add text for 400+ months
text(400, max(h.Values), '400+', 'HorizontalAlignment', 'right', 'VerticalAlignment', 'top');

% Add some statistics
avg_duration = mean(durations);
median_duration = median(durations);
text(350, max(h.Values)*0.9, sprintf('Mean: %.1f months', avg_duration), 'HorizontalAlignment', 'right');
text(350, max(h.Values)*0.8, sprintf('Median: %.1f months', median_duration), 'HorizontalAlignment', 'right');

% 2. Top 10 companies
companies = {};
for i = 1:length(all_experiences)
    exp = all_experiences{i};
    if isfield(exp, 'company') && ~isempty(exp.company)
        companies{end+1} = exp.company;
    end
end
[companyCounts, uniqueCompanies] = histcounts(categorical(companies));
[sortedCounts, sortIdx] = sort(companyCounts, 'descend');
topCompanies = uniqueCompanies(sortIdx(1:min(10,length(sortedCounts))));

figure;
bar(sortedCounts(1:min(10,length(sortedCounts))));
title('Top 10 Companies');
xlabel('Companies');
ylabel('Count');
xticks(1:length(topCompanies));
xticklabels(topCompanies);
xtickangle(45);

% 3. Word cloud of job titles
if license('test', 'Text_Analytics_Toolbox')
    titles = {};
    for i = 1:length(all_experiences)
        exp = all_experiences{i};
        if isfield(exp, 'title') && ~isempty(exp.title)
            titles{end+1} = exp.title;
        end
    end
    figure;
    wordcloud(titles);
    title('Word Cloud of Job Titles');
end

% 4. Career progression over time
current_year = year(datetime('today'));
years = current_year-50:current_year;
job_counts = zeros(size(years));

for i = 1:length(all_experiences)
    exp = all_experiences{i};
    if isfield(exp, 'starts_at') && ~isempty(exp.starts_at)
        start_year = exp.starts_at.year;
        end_year = current_year;
        if isfield(exp, 'ends_at') && ~isempty(exp.ends_at)
            end_year = exp.ends_at.year;
        end
        year_range = start_year:end_year;
        for y = year_range
            if y >= years(1) && y <= years(end)
                job_counts(y - years(1) + 1) = job_counts(y - years(1) + 1) + 1;
            end
        end
    end
end

figure;
plot(years, job_counts, 'LineWidth', 2);
title('Career Progression Over Time');
xlabel('Year');
ylabel('Number of Active Jobs');

% 5. Bar plot of most common words in job descriptions
if license('test', 'Text_Analytics_Toolbox')
    descriptions = {};
    for i = 1:length(all_experiences)
        exp = all_experiences{i};
        if isfield(exp, 'description') && ~isempty(exp.description)
            descriptions{end+1} = exp.description;
        end
    end
    words = tokenizedDocument(descriptions);
    bag = bagOfWords(words);
    
    [sortedCounts, sortIdx] = sort(bag.Counts, 'descend');
    topWords = bag.Vocabulary(sortIdx(1:20));
    topCounts = sortedCounts(1:20);
    
    figure;
    bar(1:20, topCounts);
    title('Top 20 Words in Job Descriptions');
    xlabel('Words');
    ylabel('Frequency');
    xticks(1:20);
    xticklabels(topWords);
    xtickangle(45);
end