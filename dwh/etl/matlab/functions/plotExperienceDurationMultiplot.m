function plotExperienceDurationSeparatePlots(all_experiences)
    % Calculate durations
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

    % Cap durations at 180 months aka 15 years
    durations(durations > 180) = 180;

    % 1. Histogram
    figure('Position', [100, 100, 600, 400]);
    h = histogram(durations, 15, 'Normalization', 'count');
    title('Distribution of Experience Durations');
    xlabel('Duration (months)');
    ylabel('Count (thousands)');
    xlim([0 180]);
    adjustYAxisToThousands(gca);
    addStatistics(gca, durations, h);

    % 2. Boxplot
    figure('Position', [100, 100, 600, 400]);
    [groupedData, groupLabels] = groupDataForPlot(durations);
    boxplot(groupedData, groupLabels);
    title('Boxplot of Experience Durations');
    xlabel('Duration (years)');
    ylabel('Duration (months)');
    ylim([0 180]);

    % 3. Violin plot
    figure('Position', [100, 100, 800, 400]);
    violinplot(groupedData, groupLabels);
    title('Violin Plot of Experience Durations');
    xlabel('Duration (years)');
    ylabel('Duration (months)');
    ylim([0 180]);
end

function [groupedData, groupLabels] = groupDataForPlot(durations)
    groupedData = [];
    groupLabels = [];
    for i = 1:15
        binRange = (i-1)*12 + 1 : i*12;
        groupData = durations(durations >= binRange(1) & durations <= binRange(end));
        if ~isempty(groupData)
            groupedData = [groupedData; groupData(:)];
            groupLabels = [groupLabels; repmat(i, length(groupData), 1)];
        end
    end
end

function adjustYAxisToThousands(ax)
    yticks_original = get(ax, 'YTick');
    yticks_new = yticks_original / 1000;
    set(ax, 'YTick', yticks_original);
    set(ax, 'YTickLabel', arrayfun(@(x) sprintf('%.1f', x), yticks_new, 'UniformOutput', false));
end

function addStatistics(ax, durations, h)
    avg_duration = mean(durations);
    median_duration = median(durations);
    text(ax, 150, max(h.Values)*0.9, sprintf('Mean: %.1f months', avg_duration), 'HorizontalAlignment', 'right');
    text(ax, 150, max(h.Values)*0.8, sprintf('Median: %.1f months', median_duration), 'HorizontalAlignment', 'right');
end

function duration = calcDuration(start, finish)
    if isempty(finish)
        finish = datetime('today');
    else
        finish = datetime(finish.year, finish.month, finish.day);
    end
    start = datetime(start.year, start.month, start.day);
    duration = calmonths(between(start, finish));
end

% Violin plot function (if not available in your MATLAB version)
function violinplot(data, labels)
    uniqueLabels = unique(labels);
    for i = 1:length(uniqueLabels)
        groupData = data(labels == uniqueLabels(i));
        if ~isempty(groupData)
            [f, u] = ksdensity(groupData);
            f = f/max(f)*0.3;
            fill([f -fliplr(f)]+i, [u fliplr(u)], 'b', 'FaceAlpha', 0.3);
            hold on;
        end
    end
    boxplot(data, labels, 'Colors', 'k', 'Width', 0.1);
    set(gca, 'XTick', 1:length(uniqueLabels));
    set(gca, 'XTickLabel', uniqueLabels);
end