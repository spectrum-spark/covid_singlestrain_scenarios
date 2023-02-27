
efficacy_type=1;
temp=readtable('WP4efficacylookup.csv','ReadVariableNames',true);
lookup=table2array(temp(:,[2,efficacy_type+2]));
currentVE=estimate_current_efficacy(0.99, -0.1, 0.1, lookup)

function currentVE=estimate_current_efficacy(VE0, decay_rate, time_since_vaccination, lookup)

init_neut = get_neut_from_efficacy(VE0, lookup);
current_neut = get_neut_over_time(init_neut, decay_rate,time_since_vaccination);
currentVE = get_efficacy_from_neut(current_neut, lookup);
end

function neut=get_neut_from_efficacy(VE, lookup)



loweff_ind=find(lookup(:,2)<=VE,1,'last');
higheff_ind=find(lookup(:,2)>=VE,1,'first');

if isempty(loweff_ind)
    %if neut is too low (note the file has a minimum VE against death of 0.05)
    log10neut = min(lookup(:,1));
    display('min neut hit')
elseif isempty(higheff_ind)
    log10neut = max(lookup(:,1));
    display('max neut exceeded')
else
    lowneut=lookup(loweff_ind,1);
    lowVE=lookup(loweff_ind,2);
        
    if lowVE~=VE
        %interpolate if no match
        
        highneut=lookup(higheff_ind,1);
        highVE=lookup(higheff_ind,2);

        log10neut = interp1([lowVE,highVE],[lowneut,highneut],VE);
    else
        %exact match
        log10neut = lowneut;
    end
end

neut = 10^log10neut;
end

function eff=get_efficacy_from_neut(neut, lookup)

log10neut=log10(neut);
loweff_ind=find(lookup(:,1)<=log10neut,1,'last');
higheff_ind=find(lookup(:,1)>=log10neut,1,'first');


if isempty(loweff_ind)
        eff = 0;
        display('min VE hit')
elseif isempty(higheff_ind)
        eff=1;
        display('max VE hit')
else
    lowneut=lookup(loweff_ind,1);
    lowVE=lookup(loweff_ind,2);
    if lowneut~=log10neut
        
        highneut=lookup(higheff_ind,1);
        highVE=lookup(higheff_ind,2);
        
        eff = interp1([lowneut,highneut],[lowVE,highVE],log10neut);
    else
        eff = lowVE;
        
    end
end
end


function current_neut = get_neut_over_time(starting_neut, decay_rate, time)
if (decay_rate > 0)
    decay_rate = -decay_rate;
end
current_neut = starting_neut*exp(decay_rate*time);
end
