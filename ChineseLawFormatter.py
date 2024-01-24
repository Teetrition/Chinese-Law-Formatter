import os
import re
import cn2an
import xml.dom.minidom
import time


def format_xml(input_xml):
    dom = xml.dom.minidom.parseString(input_xml)
    formatted_xml = dom.toprettyxml(indent="  ")
    return formatted_xml


def line_process(lines):
    processed_lines = []
    part_open = 0
    part_close = 0
    subpart_open = 0
    subpart_close = 0
    chapter_open = 0
    chapter_close = 0
    section_open = 0
    section_close = 0
    article_open = 0
    article_close = 0
    paragraph_open = 0
    paragraph_close = 0
    paragraph_count = 0
    suppl_exist = False

    for line in lines:
        trimmed_line = line.strip(" 　").rstrip("\n")

        if re.match(r"^第[零一二三四五六七八九十]编", trimmed_line):
            if paragraph_open - 1 == paragraph_close:
                processed_lines.append("</Paragraph>")
                paragraph_close += 1
            if article_open - 1 == article_close:
                processed_lines.append("</Article>")
                article_close += 1
            if section_open - 1 == section_close:
                processed_lines.append("</Section>")
                section_close += 1
            if chapter_open - 1 == chapter_close:
                processed_lines.append("</Chapter>")
                chapter_close += 1
            if subpart_open - 1 == subpart_close:
                processed_lines.append("</Subpart>")
                subpart_close += 1
            if part_open - 1 == part_close:
                processed_lines.append("</Part>")
                part_close += 1

            part_num = cn2an.cn2an(
                re.search(r"^第([零一二三四五六七八九十])编", trimmed_line).group(1)
            )

            processed_lines.append(
                f'<Part Num="{part_num}"><PartTitle>{trimmed_line}</PartTitle>'
            )

            part_open += 1
            # subpart_open = 0
            # subpart_close = 0
            # chapter_open = 0
            # chapter_close = 0
            # section_open = 0
            # section_close = 0

        elif re.match(r"^第[零一二三四五六七八九十]分编", trimmed_line):
            if paragraph_open - 1 == paragraph_close:
                processed_lines.append("</Paragraph>")
                paragraph_close += 1
            if article_open - 1 == article_close:
                processed_lines.append("</Article>")
                article_close += 1
            if section_open - 1 == section_close:
                processed_lines.append("</Section>")
                section_close += 1
            if chapter_open - 1 == chapter_close:
                processed_lines.append("</Chapter>")
                chapter_close += 1
            if subpart_open - 1 == subpart_close:
                processed_lines.append("</Subpart>")
                subpart_close += 1

            subpart_num = cn2an.cn2an(
                re.search(r"^第([零一二三四五六七八九十])分编", trimmed_line).group(1)
            )

            processed_lines.append(
                f'<Subpart Num="{subpart_num}"><SubpartTitle>{trimmed_line}</SubpartTitle>'
            )

            subpart_open += 1
            # section_open = 0
            # section_close = 0

        elif re.match(r"^第[零一二三四五六七八九十]{1,3}章", trimmed_line):
            if paragraph_open - 1 == paragraph_close:
                processed_lines.append("</Paragraph>")
                paragraph_close += 1
            if article_open - 1 == article_close:
                processed_lines.append("</Article>")
                article_close += 1
            if section_open - 1 == section_close:
                processed_lines.append("</Section>")
                section_close += 1
            if chapter_open - 1 == chapter_close:
                processed_lines.append("</Chapter>")
                chapter_close += 1

            chapter_num = cn2an.cn2an(
                re.search(r"^第([零一二三四五六七八九十]{1,3})章", trimmed_line).group(1)
            )

            processed_lines.append(
                f'<Chapter Num="{chapter_num}"><ChapterTitle>{trimmed_line}</ChapterTitle>'
            )

            chapter_open += 1
            # section_open = 0
            # section_close = 0

        elif re.match(r"^第[零一二三四五六七八九十]{1,3}节", trimmed_line):
            if paragraph_open - 1 == paragraph_close:
                processed_lines.append("</Paragraph>")
                paragraph_close += 1
            if article_open - 1 == article_close:
                processed_lines.append("</Article>")
                article_close += 1
            if section_open - 1 == section_close:
                processed_lines.append("</Section>")
                section_close += 1

            section_num = cn2an.cn2an(
                re.search(r"^第([零一二三四五六七八九十]{1,3})节", trimmed_line).group(1)
            )

            processed_lines.append(
                f'<Section Num="{section_num}"><SectionTitle>{trimmed_line}</SectionTitle>'
            )

            section_open += 1

        elif re.match(r"^第[零一二三四五六七八九十百千]{1,7}条(之[一二三四五六])?[ 　]+", trimmed_line):
            if paragraph_open - 1 == paragraph_close:
                processed_lines.append("</Paragraph>")
                paragraph_close += 1
            if article_open - 1 == article_close:
                processed_lines.append("</Article>")
                article_close += 1

            article_title_part1 = re.search(
                r"^(第[零一二三四五六七八九十百千]{1,7}条)(之[一二三四五六])?", trimmed_line
            ).group(1)
            article_title_part2 = re.search(
                r"^(第[零一二三四五六七八九十百千]{1,7}条)(之[一二三四五六])?", trimmed_line
            ).group(2)
            if article_title_part2:
                article_title = article_title_part1 + article_title_part2
            else:
                article_title = article_title_part1
            first_paragraph_content = re.search(
                r"^第[零一二三四五六七八九十百千]{1,7}条(之[一二三四五六])?[ 　]+(.*)$", trimmed_line
            ).group(2)
            article_num = str(
                cn2an.cn2an(
                    re.search(r"^第([零一二三四五六七八九十百千]{1,7})条", trimmed_line).group(1)
                )
            )
            article_num_branch_match = re.search(
                r"^第[零一二三四五六七八九十百千]{1,7}条(之[一二三四五六])+", trimmed_line
            )
            if article_num_branch_match:
                article_num_branch = "_" + str(
                    cn2an.cn2an(article_num_branch_match.group(1)[1:])
                )
            else:
                article_num_branch = ""

            article_num += article_num_branch

            first_paragraph_content_list = re.split(
                r"(?<=[。；])", first_paragraph_content
            )
            if len(first_paragraph_content_list) > 2:
                if first_paragraph_content_list[-1] == "":
                    first_paragraph_content_list.pop()
                sentences = ""
                for index in range(len(first_paragraph_content_list)):
                    if "但" in first_paragraph_content_list[index][0]:
                        sentences += f'<Sentence Num="{index + 1}" Function="proviso">{first_paragraph_content_list[index]}</Sentence>'
                    else:
                        sentences += f'<Sentence Num="{index + 1}">{first_paragraph_content_list[index]}</Sentence>'
                processed_lines.append(
                    f'<Article Num="{article_num}"><ArticleTitle>{article_title}</ArticleTitle><Paragraph Num="1"><ParagraphNum/><ParagraphSentence>{sentences}</ParagraphSentence>'
                )
            else:
                processed_lines.append(
                    f'<Article Num="{article_num}"><ArticleTitle>{article_title}</ArticleTitle><Paragraph Num="1"><ParagraphNum/><ParagraphSentence><Sentence>{first_paragraph_content}</Sentence></ParagraphSentence>'
                )

            article_open += 1
            paragraph_open += 1
            paragraph_count = 1

        elif re.match(r"^[\(（][零一二三四五六七八九十]{1,3}[\)）]", trimmed_line):
            item_title = re.search(
                r"^([\(（][零一二三四五六七八九十]{1,3}[\)）])", trimmed_line
            ).group(1)
            item_content = re.search(
                r"^[\(（][零一二三四五六七八九十]{1,3}[\)）](.*)$", trimmed_line
            ).group(1)
            item_num = cn2an.cn2an(
                re.search(r"^[\(（]([零一二三四五六七八九十]{1,3})[\)）]", trimmed_line).group(1)
            )

            item_content_list = re.split(r"(?<=[。；])", item_content)
            if len(item_content_list) > 2:
                if item_content_list[-1] == "":
                    item_content_list.pop()
                sentences = ""
                for index in range(len(item_content_list)):
                    if "但" in item_content_list[index][0]:
                        sentences += f'<Sentence Num="{index + 1}" Function="proviso">{item_content_list[index]}</Sentence>'
                    else:
                        sentences += f'<Sentence Num="{index + 1}">{item_content_list[index]}</Sentence>'
                processed_lines.append(
                    f'<Item Num="{item_num}"><ItemTitle>{item_title}</ItemTitle><ItemSentence>{sentences}</ItemSentence></Item>'
                )
            else:
                processed_lines.append(
                    f'<Item Num="{item_num}"><ItemTitle>{item_title}</ItemTitle><ItemSentence><Sentence>{item_content}</Sentence></ItemSentence></Item>'
                )

        elif re.match(r"^附[ 　]*则$", trimmed_line):
            suppl_exist = True
            break

        else:
            if paragraph_open - 1 == paragraph_close:
                processed_lines.append("</Paragraph>")
                paragraph_close += 1
            paragraph_count += 1

            trimmed_line_list = re.split(r"(?<=[。；])", trimmed_line)
            if len(trimmed_line_list) > 2:
                if trimmed_line_list[-1] == "":
                    trimmed_line_list.pop()
                sentences = ""
                for index in range(len(trimmed_line_list)):
                    if "但" in trimmed_line_list[index][0]:
                        sentences += f'<Sentence Num="{index + 1}" Function="proviso">{trimmed_line_list[index]}</Sentence>'
                    else:
                        sentences += f'<Sentence Num="{index + 1}">{trimmed_line_list[index]}</Sentence>'
                processed_lines.append(
                    f'<Paragraph Num="{paragraph_count}"><ParagraphNum/><ParagraphSentence>{sentences}</ParagraphSentence>'
                )
            else:
                processed_lines.append(
                    f'<Paragraph Num="{paragraph_count}"><ParagraphNum/><ParagraphSentence><Sentence>{trimmed_line}</Sentence></ParagraphSentence>'
                )

            paragraph_open += 1

    if paragraph_open - 1 == paragraph_close:
        processed_lines.append("</Paragraph>")
    if article_open - 1 == article_close:
        processed_lines.append("</Article>")
    if section_open - 1 == section_close:
        processed_lines.append("</Section>")
    if chapter_open - 1 == chapter_close:
        processed_lines.append("</Chapter>")
    if subpart_open - 1 == subpart_close:
        processed_lines.append("</Subpart>")
    if part_open - 1 == part_close:
        processed_lines.append("</Part>")

    return processed_lines, suppl_exist


def suppl_process(lines):
    start_processing = False
    suppl_lines = []
    for line in lines:
        trimmed_line = line.strip(" 　").rstrip("\n")

        if re.match(r"^附[ 　]*则$", trimmed_line):
            start_processing = True
            continue
        if start_processing:
            suppl_lines.append(line)

    return suppl_lines


if __name__ == "__main__":
    input_file_name = input("请指定本目录下要处理的纯文本文件的文件名（推荐格式为“法律名称.txt”）：")

    start_time = time.time()

    output_file_name = input_file_name.split(".")[0] + "_formatted.xml"

    input_file_path = os.path.join(os.getcwd(), input_file_name)

    try:
        with open(input_file_path, "r", encoding="utf-8") as file:
            lines = [line for line in file.readlines() if line.strip()]

        processed_lines, suppl_exist = line_process(lines)

        if not suppl_exist:
            xml_text = f'<Law><LawBody><MainProvision><LawTitle>{input_file_name.split(".")[0]}</LawTitle>{"".join(processed_lines)}</MainProvision></LawBody></Law>'
        else:
            suppl_lines = suppl_process(lines)
            processed_suppl_lines, _ = line_process(suppl_lines)
            xml_text = f'<Law><LawBody><MainProvision><LawTitle>{input_file_name.split(".")[0]}</LawTitle>{"".join(processed_lines)}</MainProvision><SupplProvision><SupplProvisionLabel>附则</SupplProvisionLabel>{"".join(processed_suppl_lines)}</SupplProvision></LawBody></Law>'

        formatted_xml = format_xml(xml_text)

        with open(output_file_name, "w", encoding="utf-8") as file:
            file.write(formatted_xml)

        print(f"处理成功。已输出到同目录下的“{output_file_name}”。")

        end_time = time.time()

        run_time = end_time - start_time

        print("程序运行时间为：{:.3f}秒".format(run_time))

    except FileNotFoundError:
        print(f"指定的文件不存在，请检查输入。")