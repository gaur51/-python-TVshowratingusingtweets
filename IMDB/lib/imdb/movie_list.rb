module Imdb

  class MovieList
    def movies
      @movies ||= parse_movies
    end

    private

    def parse_movies
      document.search("a[@href^='/title/tt']").reject do |element|
        element.inner_html.imdb_strip_tags.empty? ||
        element.inner_html.imdb_strip_tags == 'X' ||
        element.parent.inner_html =~ /media from/i
      end.map do |element|
        id = element['href'][/\d+/]

        data = element.parent.inner_html.split('<br />') #??
        title = (!data[0].nil? && !data[1].nil? && data[0] =~ /img/) ? data[1] : data[0]

#         201.
#             <a href="/title/tt0046911/?pf_rd_m=A2FGELUUNOQJNL&amp;pf_rd_p=2398042102&amp;pf_rd_r=0VZETS3QNZ33D5NYPD5V&amp;pf_rd_s=center-1&amp;pf_rd_t=15506&amp;pf_rd_i=top&amp;ref_=chttp_tt_201" title="Henri-Georges Clouzot (dir.), Simone Signoret, Véra Clouzot">Diabolique</a>
#         <span class="secondaryInfo">(1955)</span>
#
#
#
#         <span name="rk" data-value="202"></span>
#     <span name="ir" data-value="8.044788108047122"></span>
#         <span name="us" data-value="4.074624E11"></span>
#     <span name="nv" data-value="165751"></span>
#         <span name="ur" data-value="-2.955211891952878"></span>
# <a href="/title/tt0083987/?pf_rd_m=A2FGELUUNOQJNL&amp;pf_rd_p=2398042102&amp;pf_rd_r=0VZETS3QNZ33D5NYPD5V&amp;pf_rd_s=center-1&amp;pf_rd_t=15506&amp;pf_rd_i=top&amp;ref_=chttp_tt_202"> <img src="http://ia.media-imdb.com/images/M/MV5BMTQyNTQ4MTAzNl5BMl5BanBnXkFtZTcwMjk2Njk3OA@@._V1_UX45_CR0,0,45,67_AL_.jpg" width="45" height="67">
# </a>

        title = title.imdb_strip_tags.imdb_unescape_html
        title.gsub!(/\s+\(\d\d\d\d\)$/, '')

        if title =~ /\saka\s/
          titles = title.split(/\saka\s/)
          title = titles.shift.strip.imdb_unescape_html
        end

        !title.strip.blank? ? [id, title] : nil
      end.compact.uniq.map do |values|
        Imdb::Movie.new(*values)
      end
    end
  end # MovieList
end # Imdb
