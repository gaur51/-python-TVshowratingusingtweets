$LOAD_PATH.unshift(File.dirname(__FILE__)) unless
    $LOAD_PATH.include?(File.dirname(__FILE__)) || $LOAD_PATH.include?(File.expand_path(File.dirname(__FILE__)))
#$LOAD_PATH << '.'

require 'lib/imdb'


class TopTV < Imdb::MovieList
  private
  def document
    @document ||= Nokogiri::HTML(open('http://akas.imdb.com/chart/tvmeter'))
  end
end
# tv.title


def write_file_topTV
  topTVFile = File.new("topTV.csv", "w")
  $topTVs.each do |tv|
    topTVFile.puts tv.title.split(/\n/)[0] + ', ' + tv.id + ', '  + tv.url
  end
  topTVFile.close
end


def write_file_topTV_complete

  $myjson = {"tv_list" => [] }
  count = 0
  $topTVs.each do |tv|
    title = tv.title.split(/\n/)[0]
    mytv = {:title => title, :id => tv.id, :aka => tv.also_known_as, :url => tv.url, :cast_characters => tv.cast_characters, :cast_member_ids => tv.cast_member_ids, :cast_members => tv.cast_members, :cast_members_characters => tv.cast_members_characters, :company => tv.company, :countries => tv.countries, :director => tv.director, :filming_locations => tv.filming_locations, :genres => tv.genres, :languages => tv.languages, :length => tv.length, :mpaa_rating => tv.mpaa_rating, :plot => tv.plot, :plot_summary => tv.plot_summary, :plot_synopsis => tv.plot_synopsis, :poster => tv.poster, :rating => tv.rating, :release_date => tv.release_date, :tagline => tv.tagline, :trailer_url => tv.trailer_url, :votes => tv.votes, :writers => tv.writers, :year => tv.year }
    $myjson["tv_list"].push(mytv)
    sleep(1)
    count += 1
    puts count
  end

  require 'json'
  topTVCharactersFile = File.new("topTVComplete.json", "w")
  topTVCharactersFile.puts JSON.generate($myjson)
  topTVCharactersFile.close
end


def main
  $topTVs = TopTV.new.movies
  # write_file_topTV
  write_file_topTV_complete
end

main

if __FILE__ == 0
  main
end