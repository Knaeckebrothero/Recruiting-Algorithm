% 1. Bar plot of top occupations
occupations = {collection.occupation};
[occCounts, uniqueOcc] = histcounts(categorical(occupations));
[sortedCounts, sortIdx] = sort(occCounts, 'descend');
topOcc = uniqueOcc(sortIdx(1:10));

figure;
bar(sortedCounts(1:10));
title('Top 10 Occupations');
xlabel('Occupations');
ylabel('Count');
xticks(1:10);
xticklabels(topOcc);
xtickangle(45);

% 2. Pie chart of countries
countries = {collection.country_full_name};
[countryCounts, uniqueCountries] = histcounts(categorical(countries));
[sortedCounts, sortIdx] = sort(countryCounts, 'descend');
topCountries = uniqueCountries(sortIdx(1:5));  % Top 5 countries
topCounts = sortedCounts(1:5);
otherCount = sum(sortedCounts(6:end));

figure;
pie([topCounts, otherCount], [topCountries, "Other"]);
title('Distribution of Countries');

% 5. Histogram of number of connections
connections = str2double({collection.connections});
connections(isnan(connections)) = [];  % Remove any non-numeric values

figure;
histogram(connections, 20);
title('Distribution of Number of Connections');
xlabel('Number of Connections');
ylabel('Count');

% 6. Bar plot of languages
languages = [collection.languages];
[langCounts, uniqueLang] = histcounts(categorical(languages));
[sortedCounts, sortIdx] = sort(langCounts, 'descend');
topLang = uniqueLang(sortIdx(1:10));

figure;
bar(sortedCounts(1:10));
title('Top 10 Languages');
xlabel('Languages');
ylabel('Count');
xticks(1:10);
xticklabels(topLang);
xtickangle(45);