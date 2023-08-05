import logging

from Giveme5W1H.extractor.document import Document
from Giveme5W1H.extractor.extractor import MasterExtractor

"""
This is a simple example how to use the extractor in combination with a dict in news-please format.

- Nothing is cached

"""

# don`t forget to start up core_nlp_host
# giveme5w1h-corenlp

title = "Martian rock named for Rolling StonesRolling Stones get name on little Martian rock that rolled. "
lead = ""
text = """PASADENA, Calif. - There is now a Rolling Stones Rock on Mars, and it's giving Mick, Keith and the boys some serious satisfaction.NASA named a little stone for the legendary rockers after its InSight robotic lander captured it rolling across the surface of Mars last year, and the new moniker was made public at Thursday night's Rolling Stones' concert at the Rose Bowl.NASA has given us something we have always dreamed of, our very own rock on Mars. I can't believe it, Mick Jagger told the crowd after grooving through a rendition of Tumbling Dice. I want to bring it back and put it on our mantelpiece.Robert Downey Jr. announced the name, taking the stage just before the band's set at the Southern California stadium that is just a stone's throw from NASA's Jet Propulsion Laboratory, which manages InSight.Cross-pollinating science and a legendary rock band is always a good thing, the Iron Man actor said backstage.He told the crowd that JPL scientists had come up with the name in a fit of fandom and clever association.Charlie, Ronnie, Keith and Mick - they were in no way opposed to the notion, Downey said, but in typical egalitarian fashion, they suggested I assist in procuring 60,000 votes to make it official, so that's my mission.He led the audience in a shout of aye before declaring the deed done.Jagger later said, I want to say a special thanks to our favorite action man Robert Downey Jr. That was a very nice intro he gave.The rock, just a little bigger than a golf ball, was moved by InSight's own thrusters as the robotic lander touched down on Mars on Nov. 26.It only moved about 3 feet, but that's the farthest NASA has seen a rock roll while landing a craft on another planet.I've seen a lot of Mars rocks over my career, Matt Golombek, a JPL geologist who has helped NASA land all its Mars missions since 1997, said in a statement. This one probably won't be in a lot of scientific papers, but it's definitely one of the coolest.The Rolling Stones and NASA logos were shown side by side in the run-up to the show as the sun set over the Rose Bowl, leaving many fans perplexed as to what the connection was before it was announced.The concert had originally been scheduled for spring, before the Stones postponed their No Filter North American tour because Jagger had heart surgery.
"""
date_publish = '2019-08-24'

if __name__ == '__main__':
    # logger setup
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)

    # giveme5w setup - with defaults
    extractor = MasterExtractor()
    doc = Document.from_text(title + lead + text, date_publish)

    doc = extractor.parse(doc)

    top_who_answer = doc.get_top_answer('who').get_parts_as_text()
    top_what_answer = doc.get_top_answer('what').get_parts_as_text()
    top_when_answer = doc.get_top_answer('when').get_parts_as_text()
    top_where_answer = doc.get_top_answer('where').get_parts_as_text()
    top_why_answer = doc.get_top_answer('why').get_parts_as_text()
    top_how_answer = doc.get_top_answer('how').get_parts_as_text()

    print(top_who_answer)
    print(top_what_answer)
    print(top_when_answer)
    print(top_where_answer)
    print(top_why_answer)
    print(top_how_answer)
