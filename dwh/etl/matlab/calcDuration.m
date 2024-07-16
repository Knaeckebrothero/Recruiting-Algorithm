% Function to calculate experience duration in months
function duration = calcDuration(start, finish)
    if isempty(finish)
        finish = datetime('today');
    else
        finish = datetime(finish.year, finish.month, finish.day);
    end
    start = datetime(start.year, start.month, start.day);
    duration = calmonths(between(start, finish));
end