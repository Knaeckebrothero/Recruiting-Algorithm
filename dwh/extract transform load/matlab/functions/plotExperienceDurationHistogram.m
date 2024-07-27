function plotExperienceDurationHistogram(all_experiences)
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

    % Create figure
    figure;
    h = histogram(durations, 15); % One bin for every year
    title('Distribution of Experience Durations');
    xlabel('Duration (months)');
    ylabel('Count (thousands)');
    xlim([0 180]);

    % Adjust y-axis to display in thousands
    yticks_original = get(gca, 'YTick');
    yticks_new = yticks_original / 1000;
    set(gca, 'YTick', yticks_original);
    set(gca, 'YTickLabel', arrayfun(@(x) sprintf('%.1f', x), yticks_new, 'UniformOutput', false));

    % Add text for 180+ months
    text(180, max(h.Values), '180+', 'HorizontalAlignment', 'right', 'VerticalAlignment', 'top');

    % Add some statistics
    avg_duration = mean(durations);
    median_duration = median(durations);
    text(150, max(h.Values)*0.9, sprintf('Mean: %.1f months', avg_duration), 'HorizontalAlignment', 'right');
    text(150, max(h.Values)*0.8, sprintf('Median: %.1f months', median_duration), 'HorizontalAlignment', 'right');
end

% Helper function to calculate duration
function duration = calcDuration(start, finish)
    if isempty(finish)
        finish = datetime('today');
    else
        finish = datetime(finish.year, finish.month, finish.day);
    end
    start = datetime(start.year, start.month, start.day);
    duration = calmonths(between(start, finish));
end